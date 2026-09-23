import argparse

from src.rag.retrievers.hybrid_retriever import search_hybrid_chunks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search product chunks with semantic + BM25 hybrid retrieval."
    )
    parser.add_argument("query", help="User question or search query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--candidate-k", type=int, default=10)
    parser.add_argument("--semantic-threshold", type=float, default=0.0)
    args = parser.parse_args()

    results = search_hybrid_chunks(
        args.query,
        top_k=args.top_k,
        candidate_k=args.candidate_k,
        semantic_score_threshold=args.semantic_threshold,
    )
    if not results:
        print("Hybrid sonucu bulunamadı.")
        return

    for index, (document, score) in enumerate(results, start=1):
        print(f"\n--- Hybrid Result {index} | rrf_score={score:.6f} ---")
        print(f"metadata: {document.metadata}")
        print(document.page_content[:1200])


if __name__ == "__main__":
    main()
