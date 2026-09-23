import argparse

from src.rag.retrievers.product_retriever import get_product_retriever


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search with the production product retriever flow."
    )
    parser.add_argument("query", help="User question or search query")
    args = parser.parse_args()

    # Bu script, chatbotun ana product_retriever akışını test eder.
    retriever = get_product_retriever()
    documents = retriever.invoke(args.query)

    if not documents:
        print("Product retriever sonucu bulunamadı.")
        return

    for index, document in enumerate(documents, start=1):
        print(f"\n--- Product Retriever Result {index} ---")
        print(f"metadata: {document.metadata}")
        print(document.page_content[:1200])


if __name__ == "__main__":
    main()
