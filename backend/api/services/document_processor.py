from rag.models import DocumentVersion, Chunk
from api.services.embedding_service import generate_embedding


DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50


def extract_text(file_content):
    return file_content.decode("utf-8")


def create_chunks(
    text,
    chunk_size=DEFAULT_CHUNK_SIZE,
    chunk_overlap=DEFAULT_CHUNK_OVERLAP,
):
    if not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("Chunk overlap must be smaller than chunk size.")

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]

        if chunk_text.strip():
            chunks.append({
                "text": chunk_text,
                "chunk_index": chunk_index,
                "start_offset": start,
                "end_offset": min(end, len(text)),
            })

            chunk_index += 1

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def process_document_version(document_version, file_content):
    document_version.processing_status = "processing"
    document_version.save(update_fields=["processing_status"])

    try:
        extracted_text = extract_text(file_content)

        document_version.extracted_text = extracted_text
        document_version.save(update_fields=["extracted_text"])

        chunks = create_chunks(extracted_text)

        chunk_objects = []

        for chunk in chunks:
            embedding = generate_embedding(chunk["text"])

            chunk_objects.append(
                Chunk(
                    document_version=document_version,
                    text=chunk["text"],
                    chunk_index=chunk["chunk_index"],
                    start_offset=chunk["start_offset"],
                    end_offset=chunk["end_offset"],
                    chunking_config={
                        "strategy": "fixed_character",
                        "chunk_size": DEFAULT_CHUNK_SIZE,
                        "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
                    },
                    embedding=embedding,
                )
            )

        Chunk.objects.bulk_create(chunk_objects)

        document_version.processing_status = "ready"
        document_version.save(update_fields=["processing_status"])

    except Exception:
        document_version.processing_status = "failed"
        document_version.save(update_fields=["processing_status"])
        raise