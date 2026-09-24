"""Compare the same retrieval candidates with and without CrossEncoder reranking."""

from __future__ import annotations

import time

from langchain_core.runnables import RunnableLambda, RunnableParallel
from qdrant_client import models

from src.core.config import get_settings
from src.rag.rerankers.cross_encoder import rerank_documents
from src.rag.retrievers.product_retriever import (
    get_bm25_retriever,
    merge_retrieval_candidates,
)
from src.rag.vectorstores.qdrant import get_vector_store


TESTS = [
    (
        "Grundig bilgisayarda 8GB DDR3 sistem RAM'i var mı?",
        "GRUNDIG",
        lambda d: "8GB DDR3" in d.page_content and "Bellek" in d.page_content,
    ),
    (
        "Grundig bilgisayarda HDD 1TB mı?",
        "GRUNDIG",
        lambda d: "1TB" in d.page_content and "HDD" in d.page_content,
    ),
    (
        "Samsung Galaxy Z Fold 8'de ekran görüntüsü nasıl alınır?",
        "SAMSUNG-Z-FOLD-8",
        lambda d: "Ekran görüntüsü yakalama" in d.metadata.get("h2", ""),
    ),
    (
        "Samsung Galaxy Z Fold 8'in ana ekranı kaç inç?",
        "SAMSUNG-Z-FOLD-8",
        lambda d: "203.1mm" in d.page_content or "8.0" in d.page_content,
    ),
    (
        "iPhone 16 hangi depolama seçeneklerine sahip?",
        "APPLE-IPHONE-16",
        lambda d: "128 GB" in d.page_content and "256 GB" in d.page_content,
    ),
    (
        "iPhone 14 kaç gram?",
        "APPLE-IPHONE-14",
        lambda d: "172 gram" in d.page_content,
    ),
]


def _build_baseline_retriever(product_id: str):
    settings = get_settings()
    product_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.product_id",
                match=models.MatchValue(value=product_id),
            )
        ]
    )
    semantic = get_vector_store().as_retriever(
        search_kwargs={
            "k": settings.hybrid_branch_k,
            "score_threshold": settings.retrieval_score_threshold,
            "filter": product_filter,
        }
    )
    keyword = get_bm25_retriever(product_id)
    return RunnableParallel(
        semantic=semantic,
        keyword=keyword,
    ) | RunnableLambda(merge_retrieval_candidates)


def _rank(documents, predicate) -> int | None:
    for rank, document in enumerate(documents, start=1):
        if predicate(document):
            return rank
    return None


def _recall(ranks: list[int | None], limit: int) -> float:
    return sum(rank is not None and rank <= limit for rank in ranks) / len(ranks)


def _mrr(ranks: list[int | None]) -> float:
    return sum(1 / rank for rank in ranks if rank is not None) / len(ranks)


def main() -> None:
    baseline_ranks: list[int | None] = []
    reranked_ranks: list[int | None] = []

    for question, product_id, predicate in TESTS:
        baseline_retriever = _build_baseline_retriever(product_id)

        start = time.perf_counter()
        baseline = baseline_retriever.invoke(question)
        baseline_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        reranked = rerank_documents(
            question,
            baseline,
            top_k=get_settings().top_k,
        )
        reranker_ms = (time.perf_counter() - start) * 1000

        baseline_rank = _rank(baseline, predicate)
        reranked_rank = _rank(reranked, predicate)
        baseline_ranks.append(baseline_rank)
        reranked_ranks.append(reranked_rank)

        print(f"\nQUESTION: {question}")
        print(f"BASELINE: rank={baseline_rank} latency={baseline_ms:.0f}ms")
        print(f"RERANKED: rank={reranked_rank} added_latency={reranker_ms:.0f}ms")
        print(
            "RERANKED TOP: "
            + " | ".join(
                f"{d.metadata.get('source_type')} / {d.metadata.get('h2')}"
                for d in reranked[:3]
            )
        )

    print("\n=== SUMMARY ===")
    for label, ranks in (("BASELINE", baseline_ranks), ("RERANKED", reranked_ranks)):
        print(
            f"{label}: Recall@1={_recall(ranks, 1):.2f} "
            f"Recall@3={_recall(ranks, 3):.2f} "
            f"Recall@5={_recall(ranks, 5):.2f} "
            f"MRR={_mrr(ranks):.2f} ranks={ranks}"
        )


if __name__ == "__main__":
    main()
