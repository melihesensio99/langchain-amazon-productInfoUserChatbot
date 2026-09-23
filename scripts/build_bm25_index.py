from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents
from src.rag.retrievers.bm25_index import save_bm25_retriever


if __name__ == "__main__":
    documents = load_processed_markdown("data/processed")
    chunks = split_markdown_documents(documents)
    save_bm25_retriever(chunks)
    print(f"BM25 index oluşturuldu. Chunk sayısı: {len(chunks)}")
