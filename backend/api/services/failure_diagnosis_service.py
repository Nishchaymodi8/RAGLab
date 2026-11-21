from api.services.retrieval_metrics_service import (
    calculate_recall_at_k,
    calculate_hit_rate_at_k,
)


from api.services.retrieval_metrics_service import (
    calculate_recall_at_k,
    calculate_precision_at_k,
    calculate_hit_rate_at_k,
    calculate_mrr,
    calculate_ndcg_at_k,
)

from api.services.answer_metrics_service import (
    calculate_exact_match,
    calculate_token_f1,
    calculate_answer_relevance,
    calculate_answer_correctness,
)

def diagnose_retrieval_failure(
    retrieval_metrics,
):
    recall = retrieval_metrics.get("recall_at_k")
    hit_rate = retrieval_metrics.get("hit_rate_at_k")

    if recall == 0 or hit_rate == 0:
        return {
            "failure_type": "retrieval_failure",
            "severity": "high",
            "reason": "No relevant passage was retrieved.",
        }

    return None


def diagnose_generation_failure(
    answer_metrics,
):
    correctness = answer_metrics.get(
        "answer_correctness"
    )

    relevance = answer_metrics.get(
        "answer_relevance"
    )

    if (
        correctness is not None
        and correctness < 0.3
        and relevance is not None
        and relevance >= 0.5
    ):
        return {
            "failure_type": "generation_failure",
            "severity": "high",
            "reason": (
                "The answer is related to the question "
                "but has low semantic correctness."
            ),
        }

    return None

def diagnose_failure(
    retrieval_metrics,
    answer_metrics,
):
    recall = retrieval_metrics.get("recall_at_k")
    hit_rate = retrieval_metrics.get("hit_rate_at_k")

    correctness = answer_metrics.get(
        "answer_correctness"
    )

    relevance = answer_metrics.get(
        "answer_relevance"
    )

    # Retrieval ground truth is not available.
    if recall is None or hit_rate is None:
        if (
            correctness is not None
            and correctness < 0.3
            and relevance is not None
            and relevance >= 0.5
        ):
            return {
                "failure_type": "evaluation_incomplete",
                "severity": "medium",
                "reason": (
                    "The generated answer has low semantic "
                    "correctness, but retrieval relevance "
                    "cannot be determined because no "
                    "ground-truth passages are annotated."
                ),
            }

        return {
            "failure_type": "evaluation_incomplete",
            "severity": "low",
            "reason": (
                "Retrieval failure cannot be determined "
                "because no ground-truth passages are annotated."
            ),
        }

    # Retrieval failure
    if recall == 0 or hit_rate == 0:
        return {
            "failure_type": "retrieval_failure",
            "severity": "high",
            "reason": "No relevant passage was retrieved.",
        }

    # Generation failure
    if (
        correctness is not None
        and correctness < 0.3
        and relevance is not None
        and relevance >= 0.5
    ):
        return {
            "failure_type": "generation_failure",
            "severity": "high",
            "reason": (
                "Relevant passages were retrieved, but "
                "the generated answer has low semantic "
                "correctness."
            ),
        }

    return {
        "failure_type": "no_major_failure",
        "severity": "none",
        "reason": "No major failure detected.",
    }

def diagnose_evaluation_case(
    query_result,
    k=5,
):
    evaluation_case = query_result.evaluation_case

    expected_answer = evaluation_case.expected_answer

    generated_answer = query_result.generated_answer

    retrieval_metrics = {
        "recall_at_k": calculate_recall_at_k(
            query_result,
            k,
        ),
        "hit_rate_at_k": calculate_hit_rate_at_k(
            query_result,
            k,
        ),
    }

    answer_metrics = {
        "exact_match": calculate_exact_match(
            expected_answer,
            generated_answer,
        ),
        "token_f1": calculate_token_f1(
            expected_answer,
            generated_answer,
        ),
        "answer_relevance": calculate_answer_relevance(
            evaluation_case.question,
            generated_answer,
        ),
        "answer_correctness": calculate_answer_correctness(
            expected_answer,
            generated_answer,
        ),
    }

    diagnosis = diagnose_failure(
        retrieval_metrics,
        answer_metrics,
    )

    return {
        "retrieval_metrics": retrieval_metrics,
        "answer_metrics": answer_metrics,
        "diagnosis": diagnosis,
    }

def evaluate_query_result(query_result, k=5):
    evaluation_case = query_result.evaluation_case

    expected_answer = evaluation_case.expected_answer
    generated_answer = query_result.generated_answer

    retrieval_metrics = {
        "recall_at_k": calculate_recall_at_k(
            query_result,
            k,
        ),
        "precision_at_k": calculate_precision_at_k(
            query_result,
            k,
        ),
        "hit_rate_at_k": calculate_hit_rate_at_k(
            query_result,
            k,
        ),
        "mrr": calculate_mrr(
            query_result,
        ),
        "ndcg_at_k": calculate_ndcg_at_k(
            query_result,
            k,
        ),
    }

    answer_metrics = {
        "exact_match": calculate_exact_match(
            expected_answer,
            generated_answer,
        ),
        "token_f1": calculate_token_f1(
            expected_answer,
            generated_answer,
        ),
        "answer_relevance": calculate_answer_relevance(
            evaluation_case.question,
            generated_answer,
        ),
        "answer_correctness": calculate_answer_correctness(
            expected_answer,
            generated_answer,
        ),
    }

    diagnosis = diagnose_failure(
        retrieval_metrics,
        answer_metrics,
    )

    return {
        "retrieval_metrics": retrieval_metrics,
        "answer_metrics": answer_metrics,
        "diagnosis": diagnosis,
    }