from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents
from src.rag.retrievers.bm25_index import save_bm25_retriever
from src.rag.vectorstores.qdrant import sync_documents_to_qdrant
from src.rag.retrievers.product_retriever import get_bm25_retriever


class IngestionService:
    """İşlenmiş Markdown dokümanlarını chunk'layıp Qdrant'a indexler."""

    def ingest_processed_markdown(self) -> int:
        # Markdown → Document → chunk → embedding → Qdrant akışını çalıştırır.
        documents = load_processed_markdown("data/processed")
        chunks = split_markdown_documents(documents)
        # Aynı ingestion çıktısından BM25 keyword index'i de oluşturulur.
        save_bm25_retriever(chunks)
        # Çalışan process varsa eski bellekteki BM25 index'ini yenile.
        get_bm25_retriever.cache_clear()
        # Deterministik ID + stale temizliği sayesinde duplicate oluşmaz.
        sync_documents_to_qdrant(chunks)
        return len(chunks)
