from functools import lru_cache

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from src.core.config import get_settings
from langchain_community.retrievers import BM25Retriever
from qdrant_client import models

from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents
from src.rag.retrievers.bm25_index import build_bm25_retriever, load_bm25_retriever
from src.rag.rerankers.cross_encoder import rerank_documents
from src.rag.vectorstores.qdrant import get_vector_store


@lru_cache
def get_bm25_retriever(product_id: str | None = None) -> BM25Retriever:
    """Genel veya seçili ürünle sınırlandırılmış hazır BM25 retriever döndürür."""
    if product_id is None:
        # Genel aramada ingestion sırasında diske kaydedilen ortak index kullanılır.
        retriever = load_bm25_retriever()
    else:
        # Ürün sayfası chatbot'unda keyword adayları da aynı ürünle sınırlandırılır.
        documents = load_processed_markdown("data/processed")
        chunks = split_markdown_documents(documents)
        product_chunks = [
            chunk for chunk in chunks if chunk.metadata.get("product_id") == product_id
        ]
        if not product_chunks:
            raise ValueError(f"Ürün için BM25 chunk bulunamadı: {product_id}")
        retriever = build_bm25_retriever(product_chunks)

    retriever.k = max(get_settings().hybrid_branch_k, get_settings().top_k * 2)
    return retriever


def merge_retrieval_candidates(value: dict) -> list:
    """Semantic ve BM25 sonuçlarını deduplicate ederek ortak aday havuzu yapar."""
    settings = get_settings()
    candidates = []
    seen: set[str] = set()

    # Her iki kaynağın ilk adayları doğrudan korunur; RRF gibi birleştirilmiş
    # sıralama, BM25'in doğrudan bulduğu teknik chunk'ı aşağı itmez.
    for document in [
        *value["semantic"][: settings.hybrid_branch_k],
        *value["keyword"][: settings.hybrid_branch_k],
    ]:
        key = str(document.metadata.get("chunk_id") or document.page_content)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(document)
        if len(candidates) >= settings.reranker_candidate_k:
            break
    return candidates


def get_product_retriever(product_id: str | None = None):
    settings = get_settings()
    candidate_k = max(settings.hybrid_branch_k, settings.top_k * 2)
    product_filter = None
    if product_id:
        # Qdrant payload'ındaki metadata.product_id alanı ürün sayfası filtresidir.
        product_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.product_id",
                    match=models.MatchValue(value=product_id),
                )
            ]
        )

    # Qdrant tarafındaki hazır LangChain retriever semantic/dense arama yapar.
    semantic_search_kwargs = {
        "k": candidate_k,
        "score_threshold": settings.retrieval_score_threshold,
    }
    if product_filter is not None:
        semantic_search_kwargs["filter"] = product_filter

    semantic_retriever = get_vector_store().as_retriever(
        search_kwargs=semantic_search_kwargs
    )

    # LangChain'in hazır BM25Retriever bileşeni keyword aramasını yapar.
    keyword_retriever = get_bm25_retriever(product_id)

    # RRF yerine iki kolun ilk adaylarını ayrı koruruz. Böylece bir retriever'ın
    # güçlü bulduğu chunk, diğer retriever'ın sıralaması yüzünden kaybolmaz.
    candidates = RunnableParallel(
        query=RunnablePassthrough(),
        semantic=semantic_retriever,
        keyword=keyword_retriever,
    )

    return candidates | RunnableLambda(
        lambda value: rerank_documents(
            value["query"],
            merge_retrieval_candidates(value),
            top_k=settings.top_k,
        )
    )
