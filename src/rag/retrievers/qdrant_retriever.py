from qdrant_client import models
from langchain_core.documents import Document

from src.core.config import get_settings
from src.rag.vectorstores.qdrant import get_vector_store


def _build_filter(
    *,
    product_id: str | None = None,
    source_type: str | None = None,
) -> models.Filter | None:
    conditions = []

    if product_id:
        conditions.append(
            models.FieldCondition(
                key="metadata.product_id",
                match=models.MatchValue(value=product_id),
            )
        )

    if source_type:
        conditions.append(
            models.FieldCondition(
                key="metadata.source_type",
                match=models.MatchValue(value=source_type),
            )
        )

    if not conditions:
        return None

    return models.Filter(must=conditions)


def search_product_chunks(
    query: str,
    *,
    top_k: int | None = None,
    product_id: str | None = None,
    source_type: str | None = None,
) -> list[tuple[Document, float]]:
    """Return the most relevant chunks and their Qdrant scores."""
    settings = get_settings()
    limit = top_k or settings.top_k
    query_filter = _build_filter(
        product_id=product_id,
        source_type=source_type,
    )

    return get_vector_store().similarity_search_with_score(
        query,
        k=limit,
        filter=query_filter,
    )
