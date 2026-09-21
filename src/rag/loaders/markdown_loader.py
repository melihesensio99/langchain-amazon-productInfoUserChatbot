from pathlib import Path

from langchain_core.documents import Document


def _parse_frontmatter(raw_text: str) -> tuple[dict[str, str], str]:
    if not raw_text.startswith("---"):
        return {}, raw_text.strip()

    parts = raw_text.split("---", 2)
    if len(parts) != 3:
        return {}, raw_text.strip()

    metadata: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')

    return metadata, parts[2].strip()


def load_markdown_document(markdown_path: str | Path) -> Document:
    path = Path(markdown_path)
    raw_text = path.read_text(encoding="utf-8")
    metadata, content = _parse_frontmatter(raw_text)
    metadata.setdefault("source_file", path.name)
    metadata.setdefault("source_type", "markdown")
    return Document(page_content=content, metadata=metadata)


def load_processed_markdown(directory: str | Path) -> list[Document]:
    paths = sorted(
        path
        for path in Path(directory).glob("*.md")
        if not path.stem.endswith("-fresh")
    )
    return [load_markdown_document(path) for path in paths]
