from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )


def split_markdown_documents(documents):
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
    return chunks
