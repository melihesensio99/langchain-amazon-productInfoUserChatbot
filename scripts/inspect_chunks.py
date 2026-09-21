import json
from pathlib import Path

from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents


def main() -> None:
    documents = load_processed_markdown(Path("data/processed"))
    chunks = split_markdown_documents(documents)
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(json.dumps({
            "chunk": index,
            "characters": len(chunk.page_content),
            "metadata": chunk.metadata,
            "preview": chunk.page_content[:240].replace("\n", " "),
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
