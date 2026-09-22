from src.core.config import get_settings
from src.rag.vectorstores.qdrant import get_vector_store


def get_product_retriever():
    settings = get_settings()
    return get_vector_store().as_retriever(
        search_kwargs={
            # LLM'e gönderilecek en fazla aday chunk sayısı.
            "k": settings.top_k,
            # Alaka skoru düşük olan chunk'ları context'e almadan eler.
            "score_threshold": settings.retrieval_score_threshold,
        }
    )
