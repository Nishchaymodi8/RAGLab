from django.utils import timezone

from rag.models import (
    EvaluationRun,
    QueryResult,
    RetrievedPassage,
)

from api.services.retrieval_pipeline_service import retrieve
from api.services.generation_service import generate_answer

from api.services.evaluation_service import evaluate_query_result
from api.services.evaluation_persistence_service import (
    persist_evaluation_metrics,
)
from api.services.failure_diagnosis_persistence_service import (
    persist_failure_diagnosis,
)


def run_evaluation(evaluation_run):
    evaluation_run.status = "running"
    evaluation_run.started_at = timezone.now()
    evaluation_run.save(
        update_fields=["status", "started_at"]
    )

    try:
        cases = evaluation_run.dataset.evaluation_cases.all()

        for case in cases:
            start_time = timezone.now()

            rerank = evaluation_run.configuration.retrieval_params.get(
                "rerank",
                False,
            )

            retrieved_results = retrieve(
                query=case.question,
                strategy=evaluation_run.configuration.strategy,
                top_k=evaluation_run.configuration.top_k,
                rerank=rerank,
            )

            end_time = timezone.now()

            latency_ms = (
                end_time - start_time
            ).total_seconds() * 1000

            generated_answer = generate_answer(
                case.question,
                retrieved_results,
            )

            query_result = QueryResult.objects.create(
                evaluation_run=evaluation_run,
                evaluation_case=case,
                retrieval_latency_ms=latency_ms,
                retrieved_count=len(retrieved_results),
                generated_answer=generated_answer,
            )

            passages = []

            for rank, result in enumerate(
                retrieved_results,
                start=1,
            ):
                passages.append(
                    RetrievedPassage(
                        query_result=query_result,
                        chunk=result["chunk"],
                        rank=rank,
                        score=result["score"],
                    )
                )

            RetrievedPassage.objects.bulk_create(
                passages
            )
            evaluation = evaluate_query_result(
                query_result
            )

            persist_evaluation_metrics(
                evaluation_run,
                evaluation,
            )

            persist_failure_diagnosis(
                query_result,
                evaluation["diagnosis"],
            )

        evaluation_run.status = "completed"
        evaluation_run.completed_at = timezone.now()
        evaluation_run.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )

        return evaluation_run

    except Exception:
        evaluation_run.status = "failed"
        evaluation_run.completed_at = timezone.now()
        evaluation_run.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )
        raise