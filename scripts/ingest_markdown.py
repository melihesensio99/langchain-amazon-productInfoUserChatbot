from src.rag.loaders.document_loader import load_markdown_documents
from src.rag.loaders.text_splitter import get_text_splitter
from src.rag.vectorstores.qdrant import get_vector_store


if __name__ == "__main__":
    documents = load_markdown_documents("urun_katalogu.md")
    chunks = get_text_splitter().split_documents(documents)
    get_vector_store().add_documents(chunks)
    print(f"Indexed markdown chunks: {len(chunks)}")
