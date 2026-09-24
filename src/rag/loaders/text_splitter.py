import re
from collections.abc import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.normalizers.chunk_quality import analyze_chunk


_TABLE_SEPARATOR = re.compile(
    r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$"
)
_HEADING_TRAILING_RULE = re.compile(r"(?:\\_|_){3,}\s*$")


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """Tablo dışındaki düz metin bölümleri için genel splitter."""
    return RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )


def _prepend_context(chunk: Document) -> Document:
    """Belge ve başlık hiyerarşisini embedding metnine ekler."""
    metadata = chunk.metadata
    product_name = metadata.get("product_name")
    hierarchy = []

    for key in ("h1", "h2", "h3"):
        value = metadata.get(key)
        if value and value not in hierarchy:
            hierarchy.append(value)

    context_parts = []
    if product_name:
        context_parts.append(f"Belge: {product_name}")
    if hierarchy:
        context_parts.append(f"Bölüm: {' > '.join(hierarchy)}")

    if not context_parts:
        return chunk

    context = f"[{' | '.join(context_parts)}]\n\n"
    if not chunk.page_content.startswith(context):
        chunk.page_content = context + chunk.page_content
    return chunk


def _normalize_section_metadata(metadata: dict) -> dict:
    """Parser'ın başlık metadata'sındaki dekoratif çizgileri temizler."""
    normalized = dict(metadata)
    for key in ("h1", "h2", "h3"):
        value = normalized.get(key)
        if isinstance(value, str):
            normalized[key] = _HEADING_TRAILING_RULE.sub("", value).rstrip()
    return normalized


def _is_table_start(lines: list[str], index: int) -> bool:
    """Markdown tablosunun başlık + ayraç satırını tanır."""
    if index + 1 >= len(lines):
        return False
    return "|" in lines[index] and bool(_TABLE_SEPARATOR.match(lines[index + 1]))


def _collect_table(lines: list[str], start: int) -> tuple[str, int]:
    """Tabloyu satırlarıyla birlikte toplar; tablo dışındaki metne dokunmaz."""
    end = start
    while end < len(lines):
        line = lines[end].strip()
        if not line or "|" not in line:
            break
        end += 1
    return "\n".join(lines[start:end]).strip(), end


def _split_large_table(table: str, metadata: dict) -> list[Document]:
    """Uzun tabloyu başlık satırını tekrarlayarak satır gruplarına böler."""
    lines = table.splitlines()
    if len(lines) <= 2:
        return [Document(page_content=table, metadata=dict(metadata))]

    header = lines[:2]
    chunks: list[Document] = []
    current = header[:]
    for row in lines[2:]:
        candidate = "\n".join(current + [row])
        if len(candidate) > 650 and len(current) > 2:
            chunks.append(Document(page_content="\n".join(current), metadata=dict(metadata)))
            current = header[:] + [row]
        else:
            current.append(row)
    if len(current) > 2:
        chunks.append(Document(page_content="\n".join(current), metadata=dict(metadata)))
    return chunks


def _split_section_with_tables(section: Document) -> Iterable[Document]:
    """Bir Markdown bölümünü tablo ve normal metin parçalarına ayırır."""
    lines = section.page_content.splitlines()
    normal_lines: list[str] = []
    index = 0

    def flush_normal() -> Iterable[Document]:
        if not "\n".join(normal_lines).strip():
            return []
        splitter = get_text_splitter()
        return splitter.split_documents(
            [
                Document(
                    page_content="\n".join(normal_lines).strip(),
                    metadata=dict(section.metadata),
                )
            ]
        )

    while index < len(lines):
        if _is_table_start(lines, index):
            yield from flush_normal()
            normal_lines.clear()
            table, index = _collect_table(lines, index)
            yield from _split_large_table(table, section.metadata)
            continue
        normal_lines.append(lines[index])
        index += 1

    yield from flush_normal()


def _deduplicate_chunks(chunks: list[Document]) -> list[Document]:
    """Aynı belge ve bölümün birebir tekrarlarını tek chunk'a indirir."""
    seen: set[tuple[str, str, str]] = set()
    unique: list[Document] = []
    for chunk in chunks:
        normalized = re.sub(r"\s+", " ", chunk.page_content).strip()
        key = (
            str(chunk.metadata.get("product_id", "")),
            str(chunk.metadata.get("source_file", "")),
            normalized,
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(chunk)
    return unique


def split_markdown_documents(documents, *, filter_quality: bool = True):
    """Markdown başlıklarını böler, tabloları korur ve kalite filtresi uygular."""
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
        strip_headers=False,
    )

    chunks: list[Document] = []
    for document in documents:
        header_chunks = header_splitter.split_text(document.page_content)
        for section in header_chunks:
            section.metadata = _normalize_section_metadata(
                {**document.metadata, **section.metadata}
            )
            chunks.extend(_split_section_with_tables(section))

    chunks = [_prepend_context(chunk) for chunk in _deduplicate_chunks(chunks)]
    if not filter_quality:
        return chunks

    return [chunk for chunk in chunks if not analyze_chunk(chunk).should_filter]
