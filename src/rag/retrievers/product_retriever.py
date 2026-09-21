from src.core.config import get_settings
from src.rag.vectorstores.qdrant import get_vector_store


def get_product_retriever():
    return get_vector_store().as_retriever(search_kwargs={"k": get_settings().top_k})
