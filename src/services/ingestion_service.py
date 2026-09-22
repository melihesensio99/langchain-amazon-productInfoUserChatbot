from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents
from src.rag.vectorstores.qdrant import get_vector_store


class IngestionService:
    """İşlenmiş Markdown dokümanlarını chunk'layıp Qdrant'a indexler."""

    def ingest_processed_markdown(self) -> int:
        # Markdown → Document → chunk → embedding → Qdrant akışını çalıştırır.
        documents = load_processed_markdown("data/processed")
        chunks = split_markdown_documents(documents)
        get_vector_store().add_documents(chunks)
        return len(chunks)
