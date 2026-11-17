from api.services.retrieval_pipeline_service import retrieve

from api.services.generation_service import generate_answer


def run_rag(query,top_k=5,strategy="semantic",rerank=False,):
    
    retrieved_chunks = retrieve(
        query,
        strategy=strategy,
        top_k=top_k,
        rerank=rerank,
    )

    answer = generate_answer(
        query,
        retrieved_chunks,
    )

    sources = []

    for item in retrieved_chunks:
        chunk = item["chunk"]

        sources.append({
            "chunk_id": chunk.id,
            "document": chunk.document_version.document.source_name,
            "rank": len(sources) + 1,
            "score": item["score"],
            "text": chunk.text,
        })

    return {
        "query": query,
        "answer": answer,
        "sources": sources,
    }