from qdrant_client import models
from langchain_core.documents import Document

from src.core.config import get_settings
from src.rag.vectorstores.qdrant import get_vector_store


def _build_filter(*, product_id: str | None = None, source_type: str | None = None):
    conditions = []
    if product_id:
        conditions.append(models.FieldCondition(
            key="metadata.product_id",
            match=models.MatchValue(value=product_id),
        ))
    if source_type:
        conditions.append(models.FieldCondition(
            key="metadata.source_type",
            match=models.MatchValue(value=source_type),
        ))
    return models.Filter(must=conditions) if conditions else None


def search_product_chunks(
    query: str,
    *,
    top_k: int | None = None,
    score_threshold: float | None = None,
    product_id: str | None = None,
    source_type: str | None = None,
) -> list[tuple[Document, float]]:
    """Debug için Qdrant semantic aramasını skorlarıyla döndürür."""
    settings = get_settings()
    return get_vector_store().similarity_search_with_score(
        query,
        k=top_k if top_k is not None else settings.top_k,
        filter=_build_filter(product_id=product_id, source_type=source_type),
        score_threshold=(
            score_threshold
            if score_threshold is not None
            else settings.retrieval_score_threshold
        ),
    )
