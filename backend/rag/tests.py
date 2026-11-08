from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    Chunk,
    Dataset,
    Document,
    DocumentVersion,
    EvaluationCase,
    EvaluationCaseRelevance,
    EvaluationRun,
    MetricResult,
    QueryResult,
    RetrievedPassage,
    RunConfiguration,
)


class DatasetModelTests(TestCase):

    def test_dataset_creation(self):
        dataset = Dataset.objects.create(
            name="Test Dataset",
            version="1.0",
            description="Dataset for model testing",
        )

        self.assertEqual(dataset.name, "Test Dataset")
        self.assertEqual(dataset.version, "1.0")
        self.assertEqual(str(dataset), "Test Dataset v1.0")

    def test_dataset_name_and_version_must_be_unique(self):
        Dataset.objects.create(
            name="Test Dataset",
            version="1.0",
        )

        with self.assertRaises(IntegrityError):
            Dataset.objects.create(
                name="Test Dataset",
                version="1.0",
            )


class DocumentModelTests(TestCase):

    def test_document_and_version_creation(self):
        document = Document.objects.create(
            source_name="example.txt",
            source_type="txt",
        )

        version = DocumentVersion.objects.create(
            document=document,
            content_hash="a" * 64,
            extracted_text="This is test document content.",
            processing_status="ready",
        )

        self.assertEqual(document.versions.count(), 1)
        self.assertEqual(version.document, document)
        self.assertEqual(version.processing_status, "ready")

    def test_same_content_hash_cannot_be_added_twice(self):
        document = Document.objects.create(
            source_name="example.txt",
            source_type="txt",
        )

        DocumentVersion.objects.create(
            document=document,
            content_hash="b" * 64,
        )

        with self.assertRaises(IntegrityError):
            DocumentVersion.objects.create(
                document=document,
                content_hash="b" * 64,
            )


class ChunkModelTests(TestCase):

    def setUp(self):
        self.document = Document.objects.create(
            source_name="example.md",
            source_type="md",
        )

        self.version = DocumentVersion.objects.create(
            document=self.document,
            content_hash="c" * 64,
            extracted_text="Test content",
        )

    def test_chunk_creation(self):
        chunk = Chunk.objects.create(
            document_version=self.version,
            text="First chunk",
            chunk_index=0,
        )

        self.assertEqual(self.version.chunks.count(), 1)
        self.assertEqual(chunk.chunk_index, 0)

    def test_chunk_index_must_be_unique_per_version(self):
        Chunk.objects.create(
            document_version=self.version,
            text="First chunk",
            chunk_index=0,
        )

        with self.assertRaises(IntegrityError):
            Chunk.objects.create(
                document_version=self.version,
                text="Duplicate index",
                chunk_index=0,
            )


class EvaluationCaseModelTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Evaluation Dataset",
            version="1.0",
        )

        self.document = Document.objects.create(
            source_name="source.txt",
            source_type="txt",
        )

        self.version = DocumentVersion.objects.create(
            document=self.document,
            content_hash="d" * 64,
        )

        self.chunk = Chunk.objects.create(
            document_version=self.version,
            text="Relevant information",
            chunk_index=0,
        )

    def test_evaluation_case_creation(self):
        case = EvaluationCase.objects.create(
            dataset=self.dataset,
            question="What is RAG?",
            expected_answer="Retrieval-Augmented Generation",
            category="technical",
            difficulty="easy",
        )

        self.assertEqual(case.dataset, self.dataset)
        self.assertTrue(case.answer_expected)

    def test_evaluation_case_can_have_relevant_chunk(self):
        case = EvaluationCase.objects.create(
            dataset=self.dataset,
            question="What is RAG?",
        )

        relevance = EvaluationCaseRelevance.objects.create(
            evaluation_case=case,
            chunk=self.chunk,
            relevance_label=3,
            reference_quote="Relevant information",
        )

        self.assertEqual(case.relevant_passages.count(), 1)
        self.assertEqual(relevance.relevance_label, 3)


class EvaluationRunModelTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Run Dataset",
            version="1.0",
        )

        self.configuration = RunConfiguration.objects.create(
            strategy="vector",
            chunk_size=500,
            chunk_overlap=50,
            top_k=5,
            embedding_model="test-model",
            embedding_model_version="1.0",
        )

    def test_evaluation_run_creation(self):
        run = EvaluationRun.objects.create(
            dataset=self.dataset,
            configuration=self.configuration,
        )

        self.assertEqual(run.status, "pending")
        self.assertEqual(run.dataset, self.dataset)
        self.assertEqual(run.configuration, self.configuration)


class QueryResultModelTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Query Dataset",
            version="1.0",
        )

        self.configuration = RunConfiguration.objects.create(
            strategy="vector",
            top_k=5,
        )

        self.run = EvaluationRun.objects.create(
            dataset=self.dataset,
            configuration=self.configuration,
        )

        self.case = EvaluationCase.objects.create(
            dataset=self.dataset,
            question="Test question",
        )

    def test_query_result_creation(self):
        result = QueryResult.objects.create(
            evaluation_run=self.run,
            evaluation_case=self.case,
            retrieval_latency_ms=12.5,
            retrieved_count=5,
        )

        self.assertEqual(result.evaluation_run, self.run)
        self.assertEqual(result.evaluation_case, self.case)
        self.assertEqual(result.retrieved_count, 5)

    def test_same_case_cannot_be_added_twice_to_run(self):
        QueryResult.objects.create(
            evaluation_run=self.run,
            evaluation_case=self.case,
        )

        with self.assertRaises(IntegrityError):
            QueryResult.objects.create(
                evaluation_run=self.run,
                evaluation_case=self.case,
            )


class RetrievedPassageModelTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Retrieval Dataset",
            version="1.0",
        )

        self.configuration = RunConfiguration.objects.create(
            strategy="vector",
            top_k=5,
        )

        self.run = EvaluationRun.objects.create(
            dataset=self.dataset,
            configuration=self.configuration,
        )

        self.case = EvaluationCase.objects.create(
            dataset=self.dataset,
            question="Test question",
        )

        self.query_result = QueryResult.objects.create(
            evaluation_run=self.run,
            evaluation_case=self.case,
        )

        self.document = Document.objects.create(
            source_name="source.txt",
            source_type="txt",
        )

        self.version = DocumentVersion.objects.create(
            document=self.document,
            content_hash="e" * 64,
        )

        self.chunk = Chunk.objects.create(
            document_version=self.version,
            text="Retrieved content",
            chunk_index=0,
        )

    def test_retrieved_passage_creation(self):
        passage = RetrievedPassage.objects.create(
            query_result=self.query_result,
            chunk=self.chunk,
            rank=1,
            score=0.95,
        )

        self.assertEqual(passage.rank, 1)
        self.assertEqual(passage.score, 0.95)

    def test_rank_must_be_unique_per_query_result(self):
        RetrievedPassage.objects.create(
            query_result=self.query_result,
            chunk=self.chunk,
            rank=1,
        )

        with self.assertRaises(IntegrityError):
            RetrievedPassage.objects.create(
                query_result=self.query_result,
                chunk=self.chunk,
                rank=1,
            )


class MetricResultModelTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Metric Dataset",
            version="1.0",
        )

        self.configuration = RunConfiguration.objects.create(
            strategy="vector",
            top_k=5,
        )

        self.run = EvaluationRun.objects.create(
            dataset=self.dataset,
            configuration=self.configuration,
        )

    def test_metric_result_creation(self):
        metric = MetricResult.objects.create(
            evaluation_run=self.run,
            metric_name="Recall",
            k=5,
            value=0.8,
        )

        self.assertEqual(metric.metric_name, "Recall")
        self.assertEqual(metric.k, 5)
        self.assertEqual(metric.value, 0.8)

class DatasetAPITests(APITestCase):

    def test_create_dataset(self):
        data = {
            "name": "RAG Benchmark",
            "description": "Initial evaluation dataset",
            "version": "1.0",
        }

        response = self.client.post(
            "/api/datasets/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "RAG Benchmark")
        self.assertEqual(response.data["version"], "1.0")

    def test_list_datasets(self):
        Dataset.objects.create(
            name="Dataset One",
            version="1.0",
        )

        Dataset.objects.create(
            name="Dataset Two",
            version="1.0",
        )

        response = self.client.get("/api/datasets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_dataset(self):
        dataset = Dataset.objects.create(
            name="RAG Benchmark",
            version="1.0",
        )

        response = self.client.get(
            f"/api/datasets/{dataset.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "RAG Benchmark")

    def test_update_dataset(self):
        dataset = Dataset.objects.create(
            name="Old Name",
            version="1.0",
        )

        data = {
            "name": "Updated Name",
            "description": "Updated description",
            "version": "1.1",
        }

        response = self.client.put(
            f"/api/datasets/{dataset.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Name")
        self.assertEqual(response.data["version"], "1.1")

    def test_delete_dataset(self):
        dataset = Dataset.objects.create(
            name="Delete Me",
            version="1.0",
        )

        response = self.client.delete(
            f"/api/datasets/{dataset.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Dataset.objects.filter(id=dataset.id).exists()
        )

    def test_duplicate_dataset_returns_error(self):
        Dataset.objects.create(
            name="RAG Benchmark",
            version="1.0",
        )

        data = {
            "name": "RAG Benchmark",
            "version": "1.0",
        }

        response = self.client.post(
            "/api/datasets/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)