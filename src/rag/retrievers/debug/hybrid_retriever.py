from collections import defaultdict

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.rag.retrievers.debug.keyword_retriever import search_keyword_chunks
from src.rag.retrievers.debug.qdrant_retriever import search_product_chunks


def _document_key(document: Document) -> str:
    return "|".join([
        str(document.metadata.get("source_file", "")),
        str(document.metadata.get("h1", "")),
        str(document.metadata.get("h2", "")),
        document.page_content,
    ])


def _reciprocal_rank_fusion(
    result_lists: list[list[tuple[Document, float]]],
    *,
    top_k: int,
    rrf_constant: int = 60,
) -> list[tuple[Document, float]]:
    fused_scores: dict[str, float] = defaultdict(float)
    documents: dict[str, Document] = {}
    for results in result_lists:
        for rank, (document, _score) in enumerate(results, start=1):
            key = _document_key(document)
            documents[key] = document
            fused_scores[key] += 1 / (rrf_constant + rank)
    return [
        (documents[key], fused_scores[key])
        for key in sorted(fused_scores, key=fused_scores.get, reverse=True)[:top_k]
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
    """Debug için manuel semantic + BM25 + RRF araması."""
    return _reciprocal_rank_fusion(
        [
            search_product_chunks(
                query,
                top_k=candidate_k,
                score_threshold=semantic_score_threshold,
                product_id=product_id,
                source_type=source_type,
            ),
            search_keyword_chunks(
                query,
                top_k=candidate_k,
                product_id=product_id,
                source_type=source_type,
            ),
        ],
        top_k=top_k,
    )


class HybridRetriever(BaseRetriever):
    """Manuel hybrid karşılaştırma retriever'ı; ana akışta kullanılmaz."""

    final_k: int = 5
    candidate_k: int = 10
    semantic_score_threshold: float = 0.82

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> list[Document]:
        results = search_hybrid_chunks(
            query,
            top_k=self.final_k,
            candidate_k=self.candidate_k,
            semantic_score_threshold=self.semantic_score_threshold,
        )
        return [document for document, _score in results]
