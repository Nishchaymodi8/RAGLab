from api.services.retrieval_service import retrieve_chunks
from api.services.lexical_retrieval_service import retrieve_chunks_lexical
from api.services.hybrid_retrieval_service import retrieve_chunks_hybrid
from api.services.reranker_service import rerank_chunks


def retrieve(
    query,
    strategy="semantic",
    top_k=5,
    rerank=False,
):
    if strategy == "semantic":
        results = retrieve_chunks(
            query,
            top_k=top_k,
        )

    elif strategy == "lexical":
        results = retrieve_chunks_lexical(
            query,
            top_k=top_k,
        )

    elif strategy == "hybrid":
        results = retrieve_chunks_hybrid(
            query,
            top_k=top_k,
        )

    else:
        raise ValueError(
            f"Unknown retrieval strategy: {strategy}"
        )

    if rerank:
        results = rerank_chunks(
            query,
            results,
            top_k=top_k,
        )

    return results