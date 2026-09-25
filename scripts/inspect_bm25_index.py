import argparse
from pathlib import Path

from src.rag.retrievers.bm25_index import load_bm25_retriever


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect the persisted BM25 index and its term-to-chunk links."
    )
    parser.add_argument(
        "query",
        help="Query to inspect",
    )
    parser.add_argument(
        "--term",
        action="append",
        dest="terms",
        help="Term to inspect; repeat the option for multiple terms.",
    )
    args = parser.parse_args()

    retriever = load_bm25_retriever()
    vectorizer = retriever.vectorizer

    print("=== BM25 INDEX ===")
    print(f"Index file: {Path('data/indexes/bm25_retriever.pkl').resolve()}")
    print(f"Chunk count: {len(retriever.docs)}")
    print(f"Vocabulary size: {len(vectorizer.idf)}")
    print(f"Average chunk length: {vectorizer.avgdl:.2f} tokens")

    print("\n=== TERM -> CHUNK LINKS ===")
    terms = args.terms or ["vida", "42", "54", "usb-c", "backset"]
    for term in terms:
        matching_indexes = [
            index
            for index, frequencies in enumerate(vectorizer.doc_freqs)
            if term in frequencies
        ]
        print(
            f"{term!r}: idf={vectorizer.idf.get(term, 0):.4f}, "
            f"chunk_count={len(matching_indexes)}"
        )
        for index in matching_indexes[:3]:
            document = retriever.docs[index]
            print(
                f"  chunk[{index}] h2={document.metadata.get('h2')} "
                f"preview={document.page_content[:120].replace(chr(10), ' ')}"
            )

    print("\n=== BM25 QUERY SCORES ===")
    # Hazır BM25Retriever'ın gerçek query preprocessing fonksiyonunu kullanır.
    query_tokens = vectorizer.preprocess_func(args.query)
    scores = vectorizer.get_scores(query_tokens)
    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True,
    )
    print(f"Query tokens: {query_tokens}")
    for rank, index in enumerate(ranked_indexes[:5], start=1):
        document = retriever.docs[index]
        print(
            f"{rank}. score={scores[index]:.4f} "
            f"h2={document.metadata.get('h2')}"
        )


if __name__ == "__main__":
    main()
