from concurrent.futures import ThreadPoolExecutor

from api.services.document_processor import process_document_version


executor = ThreadPoolExecutor(max_workers=2)


def start_document_ingestion(document_version, file_content):
    executor.submit(
        process_document_version,
        document_version,
        file_content,
    )