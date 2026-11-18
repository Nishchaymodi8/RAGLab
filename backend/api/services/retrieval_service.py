from pgvector.django import CosineDistance

from api.services.embedding_service import generate_embedding
from rag.models import Chunk


def retrieve_chunks(query, top_k=5):
    query_embedding = generate_embedding(query)

    chunks = (
        Chunk.objects
        .select_related("document_version__document")
        .exclude(embedding=None)
        .annotate(
            distance=CosineDistance("embedding", query_embedding)
        )
        .order_by("distance")[:top_k]
    )

    results = []

    for chunk in chunks:
        results.append({
            "chunk": chunk,
            "score": float(chunk.distance),
        })

    return results