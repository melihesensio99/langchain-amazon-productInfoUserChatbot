from collections import defaultdict

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.rag.retrievers.keyword_retriever import search_keyword_chunks
from src.rag.retrievers.qdrant_retriever import search_product_chunks


def _document_key(document: Document) -> str:
    """Semantic ve BM25 sonuçlarında aynı chunk'ı tekilleştirmek için anahtar üretir."""
    metadata = document.metadata
    return "|".join(
        [
            str(metadata.get("source_file", "")),
            str(metadata.get("h1", "")),
            str(metadata.get("h2", "")),
            document.page_content,
        ]
    )


def _reciprocal_rank_fusion(
    result_lists: list[list[tuple[Document, float]]],
    *,
    top_k: int,
    rrf_constant: int = 60,
) -> list[tuple[Document, float]]:
    """Farklı ölçeklerdeki sonuç listelerini rank bilgisiyle birleştirir."""
    fused_scores: dict[str, float] = defaultdict(float)
    documents: dict[str, Document] = {}

    for results in result_lists:
        for rank, (document, _score) in enumerate(results, start=1):
            key = _document_key(document)
            documents[key] = document
            # BM25 ve cosine skorları farklı ölçekte olduğu için ham skorları
            # toplamak yerine sonuç listesindeki sıraları kullanıyoruz.
            fused_scores[key] += 1 / (rrf_constant + rank)

    ranked_keys = sorted(
        fused_scores,
        key=fused_scores.get,
        reverse=True,
    )

    return [
        (documents[key], fused_scores[key])
        for key in ranked_keys[:top_k]
    ]


def search_hybrid_chunks(
    query: str,
    *,
    top_k: int = 5,
    candidate_k: int = 10,
    semantic_score_threshold: float = 0.0,
    product_id: str | None = None,
    source_type: str | None = None,
) -> list[tuple[Document, float]]:
    """Semantic ve BM25 sonuçlarını RRF ile birleştirir."""
    semantic_results = search_product_chunks(
        query,
        top_k=candidate_k,
        # Hybrid aday havuzunu geniş tutuyoruz; final sonuç sayısını aşağıda
        # RRF sonrası top_k ile belirliyoruz.
        score_threshold=semantic_score_threshold,
        product_id=product_id,
        source_type=source_type,
    )
    keyword_results = search_keyword_chunks(query, top_k=candidate_k)

    return _reciprocal_rank_fusion(
        [semantic_results, keyword_results],
        top_k=top_k,
    )


# PROJEYE ÖZEL MANUEL TEST SINIFI: Ana chatbot akışında hazır
# EnsembleRetriever kullanılır; bu sınıf debug ve karşılaştırma içindir.
class HybridRetriever(BaseRetriever):
    """LangChain chain'leri için semantic + BM25 retriever adaptörü."""

    final_k: int = 5
    candidate_k: int = 10
    semantic_score_threshold: float = 0.82

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> list[Document]:
        # Chain bu metodu invoke() üzerinden çağırır; dışarıya yalnızca
        # birleştirilmiş Document listesi döner.
        results = search_hybrid_chunks(
            query,
            top_k=self.final_k,
            candidate_k=self.candidate_k,
            semantic_score_threshold=self.semantic_score_threshold,
        )
        return [document for document, _score in results]
