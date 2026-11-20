import math

from rag.models import EvaluationCaseRelevance


def get_relevant_chunk_ids(evaluation_case):
    return set(
        EvaluationCaseRelevance.objects.filter(
            evaluation_case=evaluation_case
        ).values_list("chunk_id", flat=True)
    )


def get_retrieved_chunk_ids(query_result, k=None):
    passages = query_result.retrieved_passages.all()

    if k is not None:
        passages = passages.filter(rank__lte=k)

    return set(
        passages.values_list("chunk_id", flat=True)
    )


def get_relevant_retrieved_chunk_ids(query_result, k=None):
    relevant_chunk_ids = get_relevant_chunk_ids(
        query_result.evaluation_case
    )

    retrieved_chunk_ids = get_retrieved_chunk_ids(
        query_result,
        k=k,
    )

    return relevant_chunk_ids.intersection(
        retrieved_chunk_ids
    )


def get_relevant_count(evaluation_case):
    return len(
        get_relevant_chunk_ids(evaluation_case)
    )


def get_retrieved_count(query_result, k=None):
    return len(
        get_retrieved_chunk_ids(
            query_result,
            k=k,
        )
    )


def get_relevant_retrieved_count(query_result, k=None):
    return len(
        get_relevant_retrieved_chunk_ids(
            query_result,
            k=k,
        )
    )


def calculate_recall_at_k(query_result, k):
    relevant_count = get_relevant_count(
        query_result.evaluation_case
    )

    if relevant_count == 0:
        return None

    relevant_retrieved_count = get_relevant_retrieved_count(
        query_result,
        k=k,
    )

    return relevant_retrieved_count / relevant_count


def calculate_precision_at_k(query_result, k):
    retrieved_count = get_retrieved_count(
        query_result,
        k=k,
    )

    if retrieved_count == 0:
        return None

    relevant_retrieved_count = get_relevant_retrieved_count(
        query_result,
        k=k,
    )

    return relevant_retrieved_count / retrieved_count


def calculate_hit_rate_at_k(query_result, k):
    relevant_count = get_relevant_count(
        query_result.evaluation_case
    )

    if relevant_count == 0:
        return None

    relevant_retrieved_count = get_relevant_retrieved_count(
        query_result,
        k=k,
    )

    return 1.0 if relevant_retrieved_count > 0 else 0.0


def calculate_mrr(query_result):
    relevant_count = get_relevant_count(
        query_result.evaluation_case
    )

    if relevant_count == 0:
        return None

    relevant_chunk_ids = get_relevant_chunk_ids(
        query_result.evaluation_case
    )

    passages = query_result.retrieved_passages.order_by("rank")

    for passage in passages:
        if passage.chunk_id in relevant_chunk_ids:
            return 1.0 / passage.rank

    return 0.0


def calculate_ndcg_at_k(query_result, k):
    relevant_count = get_relevant_count(
        query_result.evaluation_case
    )

    if relevant_count == 0:
        return None

    relevant_chunk_ids = get_relevant_chunk_ids(
        query_result.evaluation_case
    )

    passages = query_result.retrieved_passages.filter(
        rank__lte=k
    ).order_by("rank")

    dcg = 0.0

    for passage in passages:
        if passage.chunk_id in relevant_chunk_ids:
            relevance = 1
        else:
            relevance = 0

        dcg += relevance / math.log2(passage.rank + 1)

    ideal_relevant_count = min(
        relevant_count,
        k,
    )

    idcg = 0.0

    for rank in range(1, ideal_relevant_count + 1):
        idcg += 1 / math.log2(rank + 1)

    if idcg == 0:
        return 0.0

    return dcg / idcg
