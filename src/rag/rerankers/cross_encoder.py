from functools import lru_cache

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from src.core.config import get_settings


@lru_cache
def get_cross_encoder() -> CrossEncoder:
    """Reranker modelini yalnızca ilk retrieval isteğinde yükler."""
    settings = get_settings()
    return CrossEncoder(
        settings.reranker_model,
        max_length=settings.reranker_max_length,
        device=settings.embedding_device,
    )


def rerank_documents(
    query: str,
    documents: list[Document],
    *,
    top_k: int,
) -> list[Document]:
    """Semantic+BM25 adaylarını query-document alakasıyla yeniden sıralar."""
    if not documents:
        return []

    # Aday metnini sınırlamak CPU maliyetini ve CrossEncoder token taşmasını
    # kontrol eder; bölüm breadcrumb'ı page_content'in başında korunur.
    pairs = [(query, document.page_content[:4000]) for document in documents]
    scores = get_cross_encoder().predict(pairs, show_progress_bar=False)
    ranked = sorted(
        zip(scores, documents),
        key=lambda item: float(item[0]),
        reverse=True,
    )
    return [document for _, document in ranked[:top_k]]
