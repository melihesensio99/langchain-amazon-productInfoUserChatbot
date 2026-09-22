from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter

from src.rag.normalizers.chunk_quality import analyze_chunk


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )


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
    if not filter_quality:
        return chunks

    return [
        chunk
        for chunk in chunks
        if not analyze_chunk(chunk).should_filter
    ]
