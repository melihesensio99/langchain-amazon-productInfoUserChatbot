from functools import lru_cache

from langchain_core.documents import Document

from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents


def _key(document: Document) -> tuple[str, str, str, int]:
    metadata = document.metadata
    return (
        str(metadata.get("product_id", "")),
        str(metadata.get("source_file", "")),
        str(metadata.get("h2", "")),
        int(metadata.get("chunk_index", -1)),
    )


@lru_cache
def load_retrieval_corpus() -> tuple[Document, ...]:
    """Processed Markdown'ı retrieval bağlamı genişletmek için belleğe alır."""
    documents = load_processed_markdown("data/processed")
    return tuple(split_markdown_documents(documents))


def expand_with_related_context(
    candidates: list[Document],
    *,
    max_candidates: int,
    neighbor_radius: int = 1,
) -> list[Document]:
    """Aday chunk'ların aynı bölüm ve yakın komşu bağlamını ekler.

    Bu işlem ürüne veya belirli bir tabloya özel değildir. Aynı `h2` altında
    bölünmüş tablo parçalarını ve aynı PDF'deki hemen komşu parçaları reranker'a
    göndermeden önce aday havuzuna ekler.
    """
    corpus = load_retrieval_corpus()
    by_section: dict[tuple[str, str, str], list[Document]] = {}
    by_document: dict[tuple[str, str], list[Document]] = {}

    for document in corpus:
        metadata = document.metadata
        section_key = (
            str(metadata.get("product_id", "")),
            str(metadata.get("source_file", "")),
            str(metadata.get("h2", "")),
        )
        document_key = section_key[:2]
        by_section.setdefault(section_key, []).append(document)
        by_document.setdefault(document_key, []).append(document)

    for values in (*by_section.values(), *by_document.values()):
        values.sort(key=lambda item: int(item.metadata.get("chunk_index", -1)))

    result: list[Document] = []
    seen: set[tuple[str, str, str, int]] = set()

    def add(document: Document) -> None:
        identity = _key(document)
        if identity in seen or len(result) >= max_candidates:
            return
        seen.add(identity)
        result.append(document)

    # Önce doğrudan semantic/BM25 adaylarını koruyoruz.
    for candidate in candidates:
        add(candidate)

    for candidate in candidates:
        metadata = candidate.metadata
        section_key = (
            str(metadata.get("product_id", "")),
            str(metadata.get("source_file", "")),
            str(metadata.get("h2", "")),
        )
        section_chunks = by_section.get(section_key, [])
        for related in section_chunks:
            add(related)

        document_key = section_key[:2]
        document_chunks = by_document.get(document_key, [])
        position = int(metadata.get("chunk_index", -1))
        for related in document_chunks:
            related_position = int(related.metadata.get("chunk_index", -1))
            if position >= 0 and abs(related_position - position) <= neighbor_radius:
                add(related)

    return result[:max_candidates]
