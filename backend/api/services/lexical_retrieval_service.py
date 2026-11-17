from rank_bm25 import BM25Okapi

from rag.models import Chunk


def tokenize(text):
    return text.lower().split()


def retrieve_chunks_lexical(query, top_k=5):
    chunks = list(
        Chunk.objects
        .select_related("document_version__document")
        .exclude(text="")
    )

    if not chunks:
        return []

    corpus = [
        tokenize(chunk.text)
        for chunk in chunks
    ]

    bm25 = BM25Okapi(corpus)

    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_results = []

    for chunk, score in zip(chunks, scores):
        ranked_results.append({
            "chunk": chunk,
            "score": float(score),
        })

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return ranked_results[:top_k]