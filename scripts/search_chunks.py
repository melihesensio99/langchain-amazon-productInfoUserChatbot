import argparse

from src.rag.retrievers.qdrant_retriever import search_product_chunks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search relevant product chunks in Qdrant."
    )
    parser.add_argument("query", help="User question or search query")
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--score-threshold", type=float, default=None)
    parser.add_argument("--product-id")
    parser.add_argument("--source-type")
    args = parser.parse_args()

    results = search_product_chunks(
        args.query,
        top_k=args.top_k,
        score_threshold=args.score_threshold,
        product_id=args.product_id,
        source_type=args.source_type,
    )

    if not results:
        print("Sonuç bulunamadı.")
        return

    for index, (document, score) in enumerate(results, start=1):
        print(f"\n--- Result {index} | score={score:.4f} ---")
        print(f"metadata: {document.metadata}")
        print(document.page_content[:1200])


if __name__ == "__main__":
    main()
