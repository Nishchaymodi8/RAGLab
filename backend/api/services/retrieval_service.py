import numpy as np

from api.services.embedding_service import generate_embedding
from rag.models import Chunk


def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def retrieve_chunks(query, top_k=5):
    query_embedding = generate_embedding(query)

    chunks = (
        Chunk.objects
        .select_related("document_version__document")
        .exclude(embedding=None)
    )

    results = []

    for chunk in chunks:
        score = cosine_similarity(
            query_embedding,
            chunk.embedding,
        )

        results.append({
            "chunk": chunk,
            "score": score,
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]