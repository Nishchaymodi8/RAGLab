from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model = None


def get_reranker_model():
    global _model

    if _model is None:
        _model = CrossEncoder(MODEL_NAME)

    return _model


def rerank_chunks(query, retrieved_results, top_k=5):
    if not retrieved_results:
        return []

    model = get_reranker_model()

    pairs = [
        [query, result["chunk"].text]
        for result in retrieved_results
    ]

    scores = model.predict(pairs)

    reranked_results = []

    for result, score in zip(retrieved_results, scores):
        reranked_results.append({
            "chunk": result["chunk"],
            "score": float(score),
        })

    reranked_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return reranked_results[:top_k]