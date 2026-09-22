import json
from pathlib import Path

from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents
from src.rag.normalizers.chunk_quality import analyze_chunk


def main() -> None:
    documents = load_processed_markdown(Path("data/processed"))
    chunks = split_markdown_documents(documents, filter_quality=False)
    candidates = []

    for index, chunk in enumerate(chunks, start=1):
        report = analyze_chunk(chunk)
        if report.should_filter:
            candidates.append(
                {
                    "chunk": index,
                    "score": report.boilerplate_score,
                    "reasons": report.reasons,
                    "characters": report.characters,
                    "words": report.words,
                    "links": report.links,
                    "metadata": chunk.metadata,
                    "preview": chunk.page_content[:500].replace("\n", " "),
                }
            )

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Quality filter candidates: {len(candidates)}")

    for candidate in candidates:
        print(json.dumps(candidate, ensure_ascii=False))


if __name__ == "__main__":
    main()
