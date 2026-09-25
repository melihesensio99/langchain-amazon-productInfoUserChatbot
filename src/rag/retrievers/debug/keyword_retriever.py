import re
from functools import lru_cache

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents


_TOKEN_PATTERN = re.compile(r"[\wÇĞİÖŞÜçğıöşü]+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


@lru_cache
def _get_keyword_index() -> tuple[BM25Okapi, tuple[Document, ...]]:
    documents = load_processed_markdown("data/processed")
    chunks = split_markdown_documents(documents)
    return BM25Okapi([_tokenize(chunk.page_content) for chunk in chunks]), tuple(chunks)


def search_keyword_chunks(
    query: str,
    *,
    top_k: int = 5,
    product_id: str | None = None,
    source_type: str | None = None,
) -> list[tuple[Document, float]]:
    """Debug için manuel BM25 sonuçlarını skorlarıyla döndürür."""
    bm25, chunks = _get_keyword_index()
    scores = bm25.get_scores(_tokenize(query))
    ranked = sorted(range(len(chunks)), key=lambda index: scores[index], reverse=True)

    def matches(document: Document) -> bool:
        return (
            (not product_id or document.metadata.get("product_id") == product_id)
            and (
                not source_type
                or document.metadata.get("source_type") == source_type
            )
        )

    filtered = [
        index
        for index in ranked
        if scores[index] > 0 and matches(chunks[index])
    ]
    return [
        (chunks[index], float(scores[index]))
        for index in filtered[:top_k]
    ]
