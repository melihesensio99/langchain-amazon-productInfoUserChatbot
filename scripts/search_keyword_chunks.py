import argparse

from src.rag.retrievers.debug.keyword_retriever import search_keyword_chunks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search product chunks with BM25 keyword matching."
    )
    parser.add_argument("query", help="User question or keyword query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--product-id")
    parser.add_argument("--source-type")
    args = parser.parse_args()

    results = search_keyword_chunks(
        args.query,
        top_k=args.top_k,
        product_id=args.product_id,
        source_type=args.source_type,
    )
    if not results:
        print("Keyword sonucu bulunamadı.")
        return

    for index, (document, score) in enumerate(results, start=1):
        print(f"\n--- Keyword Result {index} | score={score:.4f} ---")
        print(f"metadata: {document.metadata}")
        print(document.page_content[:1200])


if __name__ == "__main__":
    main()
