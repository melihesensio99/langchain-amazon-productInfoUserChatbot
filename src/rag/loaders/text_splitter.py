from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

from src.rag.normalizers.chunk_quality import analyze_chunk


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )


def _prepend_context(chunk: Document) -> Document:
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


def split_markdown_documents(documents, *, filter_quality: bool = True):
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )
    recursive_splitter = get_text_splitter()
    chunks = []
    for document in documents:
        header_chunks = header_splitter.split_text(document.page_content)
        for chunk in header_chunks:
            chunk.metadata = {**document.metadata, **chunk.metadata}
        chunks.extend(recursive_splitter.split_documents(header_chunks))

    chunks = [_prepend_context(chunk) for chunk in chunks]

    if not filter_quality:
        return chunks

    return [
        chunk
        for chunk in chunks
        if not analyze_chunk(chunk).should_filter
    ]
