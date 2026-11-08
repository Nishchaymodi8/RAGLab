from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50)
    content_hash = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "version"],
                name="unique_dataset_name_version",
            )
        ]

    def __str__(self):
        return f"{self.name} v{self.version}"


class Document(models.Model):
    SOURCE_TYPE_CHOICES = [
        ("txt", "TXT"),
        ("md", "Markdown"),
    ]

    source_name = models.CharField(max_length=255)
    source_type = models.CharField(
        max_length=10,
        choices=SOURCE_TYPE_CHOICES,
    )
    source_uri = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source_name


class DocumentVersion(models.Model):
    PROCESSING_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    content_hash = models.CharField(max_length=64)
    extracted_text = models.TextField(blank=True)
    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "content_hash"],
                name="unique_document_content_hash",
            )
        ]

    def __str__(self):
        return f"{self.document.source_name} - {self.content_hash[:12]}"


class Chunk(models.Model):
    document_version = models.ForeignKey(
        DocumentVersion,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    text = models.TextField()
    chunk_index = models.PositiveIntegerField()
    start_offset = models.PositiveIntegerField(null=True, blank=True)
    end_offset = models.PositiveIntegerField(null=True, blank=True)
    chunking_config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_version", "chunk_index"],
                name="unique_chunk_index_per_version",
            )
        ]
        indexes = [
            models.Index(fields=["document_version", "chunk_index"]),
        ]

    def __str__(self):
        return f"Chunk {self.chunk_index}"


class EvaluationCase(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="evaluation_cases",
    )
    question = models.TextField()
    expected_answer = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    answer_expected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:80]


class EvaluationCaseRelevance(models.Model):
    evaluation_case = models.ForeignKey(
        EvaluationCase,
        on_delete=models.CASCADE,
        related_name="relevant_passages",
    )
    chunk = models.ForeignKey(
        Chunk,
        on_delete=models.PROTECT,
        related_name="evaluation_relevance",
    )
    relevance_label = models.PositiveSmallIntegerField(
        default=1,
    )
    reference_quote = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["evaluation_case", "chunk"],
                name="unique_case_chunk_relevance",
            )
        ]

    def __str__(self):
        return f"Case {self.evaluation_case_id} -> Chunk {self.chunk_id}"


class RunConfiguration(models.Model):
    strategy = models.CharField(max_length=100)
    chunk_size = models.PositiveIntegerField(null=True, blank=True)
    chunk_overlap = models.PositiveIntegerField(null=True, blank=True)
    top_k = models.PositiveIntegerField(default=5)
    embedding_model = models.CharField(max_length=200, blank=True)
    embedding_model_version = models.CharField(max_length=100, blank=True)
    retrieval_params = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.strategy


class EvaluationRun(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.PROTECT,
        related_name="evaluation_runs",
    )
    configuration = models.ForeignKey(
        RunConfiguration,
        on_delete=models.PROTECT,
        related_name="evaluation_runs",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run {self.id} - {self.dataset.name}"


class QueryResult(models.Model):
    evaluation_run = models.ForeignKey(
        EvaluationRun,
        on_delete=models.CASCADE,
        related_name="query_results",
    )
    evaluation_case = models.ForeignKey(
        EvaluationCase,
        on_delete=models.PROTECT,
        related_name="query_results",
    )
    retrieval_latency_ms = models.FloatField(null=True, blank=True)
    retrieved_count = models.PositiveIntegerField(default=0)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["evaluation_run", "evaluation_case"],
                name="unique_case_per_run",
            )
        ]

    def __str__(self):
        return f"QueryResult {self.id}"


class RetrievedPassage(models.Model):
    query_result = models.ForeignKey(
        QueryResult,
        on_delete=models.CASCADE,
        related_name="retrieved_passages",
    )
    chunk = models.ForeignKey(
        Chunk,
        on_delete=models.PROTECT,
        related_name="retrieval_results",
    )
    rank = models.PositiveIntegerField()
    score = models.FloatField(null=True, blank=True)
    relevance_label = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["query_result", "rank"],
                name="unique_rank_per_query_result",
            ),
        ]
        indexes = [
            models.Index(fields=["query_result", "rank"]),
        ]

    def __str__(self):
        return f"Rank {self.rank} - QueryResult {self.query_result_id}"


class MetricResult(models.Model):
    evaluation_run = models.ForeignKey(
        EvaluationRun,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    metric_name = models.CharField(max_length=100)
    k = models.PositiveIntegerField(null=True, blank=True)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["evaluation_run", "metric_name", "k"],
                name="unique_metric_per_run",
            )
        ]

    def __str__(self):
        return f"{self.metric_name}@{self.k}: {self.value}"