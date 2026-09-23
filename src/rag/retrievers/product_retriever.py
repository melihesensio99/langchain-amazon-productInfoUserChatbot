from functools import lru_cache

from langchain_core.runnables import RunnableLambda
from langchain_classic.retrievers import EnsembleRetriever

from src.core.config import get_settings
from langchain_community.retrievers import BM25Retriever

from src.rag.retrievers.bm25_index import load_bm25_retriever
from src.rag.vectorstores.qdrant import get_vector_store


@lru_cache
def get_bm25_retriever() -> BM25Retriever:
    """Ingestion sırasında oluşturulmuş hazır BM25Retriever'ı yükler."""
    retriever = load_bm25_retriever()
    retriever.k = max(get_settings().top_k * 2, 10)
    return retriever


def get_product_retriever():
    settings = get_settings()
    candidate_k = max(settings.top_k * 2, 10)

    # Qdrant tarafındaki hazır LangChain retriever semantic/dense arama yapar.
    semantic_retriever = get_vector_store().as_retriever(
        search_kwargs={
            "k": candidate_k,
            "score_threshold": settings.retrieval_score_threshold,
        }
    )

    # LangChain'in hazır BM25Retriever bileşeni keyword aramasını yapar.
    keyword_retriever = get_bm25_retriever()

    # EnsembleRetriever iki retriever'ın sıralamalarını RRF ile birleştirir.
    # Semantic aramayı ana yöntem (%70), BM25'i destekleyici yöntem (%30)
    # olarak ağırlıklandırıyoruz. Bu oranlar deneysel ayarlardır; retrieval
    # testlerine göre daha sonra değiştirilebilir.
    ensemble_retriever = EnsembleRetriever(
        retrievers=[semantic_retriever, keyword_retriever],
        weights=[0.7, 0.3],
    )

    # Ensemble aday havuzunu geniş tutar; chatbot'a son top_k chunk'ı veririz.
    return ensemble_retriever | RunnableLambda(
        lambda documents: documents[: settings.top_k]
    )
