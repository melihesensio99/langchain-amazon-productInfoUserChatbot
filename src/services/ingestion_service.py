from src.core.config import get_settings
from src.rag.loaders.document_loader import load_csv_documents
from src.rag.loaders.text_splitter import get_text_splitter
from src.rag.vectorstores.qdrant import get_vector_store


class IngestionService:
    def ingest_csv(self) -> int:
        settings = get_settings()
        documents = load_csv_documents(settings.csv_path)
        chunks = get_text_splitter().split_documents(documents)
        get_vector_store().add_documents(chunks)
        return len(chunks)
