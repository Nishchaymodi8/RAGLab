from api.services.retrieval_service import retrieve_chunks
from api.services.lexical_retrieval_service import retrieve_chunks_lexical


def reciprocal_rank_fusion(
    semantic_results,
    lexical_results,
    top_k=5,
    k=60,
):
    fused_scores = {}
    chunk_lookup = {}

    for rank, result in enumerate(semantic_results, start=1):
        chunk = result["chunk"]

        chunk_lookup[chunk.id] = chunk

        fused_scores.setdefault(chunk.id, 0.0)
        fused_scores[chunk.id] += 1 / (k + rank)

    for rank, result in enumerate(lexical_results, start=1):
        chunk = result["chunk"]

        chunk_lookup[chunk.id] = chunk

        fused_scores.setdefault(chunk.id, 0.0)
        fused_scores[chunk.id] += 1 / (k + rank)

    ranked_results = []

    for chunk_id, score in fused_scores.items():
        ranked_results.append({
            "chunk": chunk_lookup[chunk_id],
            "score": score,
        })

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return ranked_results[:top_k]


def retrieve_chunks_hybrid(query, top_k=5):
    semantic_results = retrieve_chunks(
        query,
        top_k=top_k,
    )

    lexical_results = retrieve_chunks_lexical(
        query,
        top_k=top_k,
    )

    return reciprocal_rank_fusion(
        semantic_results,
        lexical_results,
        top_k=top_k,
    )