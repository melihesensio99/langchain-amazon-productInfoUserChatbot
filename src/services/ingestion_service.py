from pathlib import Path

from src.rag.loaders.docling_loader import convert_pdf_to_markdown
from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.normalizers.product_markdown_formatter import format_product_markdown
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

    def ingest_product_pdf(self, *, product_id: str, product_name: str, pdf_path: str) -> int:
        """Convert one uploaded PDF, persist its normalized Markdown, then reindex."""
        source = Path(pdf_path)
        if not source.exists():
            raise FileNotFoundError(f"PDF bulunamadı: {source}")

        raw_dir = Path("data/raw")
        processed_dir = Path("data/processed")
        raw_dir.mkdir(parents=True, exist_ok=True)
        processed_dir.mkdir(parents=True, exist_ok=True)

        raw_markdown = convert_pdf_to_markdown(source)
        raw_path = raw_dir / f"{product_id}-raw.md"
        processed_path = processed_dir / f"{product_id}.md"
        raw_path.write_text(raw_markdown, encoding="utf-8")
        processed_path.write_text(
            format_product_markdown(
                raw_markdown,
                product_id=product_id,
                product_name=product_name,
                source_type="product_manual",
                source_file=source.name,
            ),
            encoding="utf-8",
        )

        # Rebuild the shared indexes from the complete processed source of truth.
        return self.ingest_processed_markdown()
