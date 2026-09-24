"""Run a small retrieval baseline against the current product collection."""

from src.rag.retrievers.product_retriever import get_product_retriever


TESTS = [
    ("Z Fold 8 kamera çözünürlüğü nedir?", "SAMSUNG-Z-FOLD-8", "technical_specs"),
    ("Z Fold 8'de ekran görüntüsü nasıl alınır?", "SAMSUNG-Z-FOLD-8", "user_manual"),
    ("iPhone 16 hangi depolama seçeneklerine sahip?", "APPLE-IPHONE-16", "technical_specs"),
    ("AirPods Max 2 hangi ses teknolojilerini destekliyor?", "APPLE-AIRPODS-MAX-2", "technical_specs"),
    ("MSI monitörün ayağı nasıl takılır?", "MSI", "technical_and_manual"),
    ("94-203 FHD LCD TV'de panel kilidi nasıl açılır?", "TV-94-203-FHD-LCD", "technical_and_manual"),
]


def main() -> None:
    retriever = get_product_retriever()

    for question, expected_product, expected_source in TESTS:
        documents = retriever.invoke(question)
        print(f"\nQUESTION: {question}")
        print(f"EXPECTED: product={expected_product}, source={expected_source}")

        if not documents:
            print("RESULT: NONE")
            continue

        for rank, document in enumerate(documents[:3], start=1):
            metadata = document.metadata
            print(
                f"RESULT {rank}: "
                f"product={metadata.get('product_id')} "
                f"source={metadata.get('source_type')} "
                f"h2={metadata.get('h2')}"
            )


if __name__ == "__main__":
    main()
