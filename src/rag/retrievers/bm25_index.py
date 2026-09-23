import pickle
import re
from pathlib import Path

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


_project_root = Path(__file__).resolve().parents[3]
_index_path = _project_root / "data" / "indexes" / "bm25_retriever.pkl"
_token_pattern = re.compile(r"[\wÇĞİÖŞÜçğıöşü]+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    """Hazır BM25Retriever için Türkçe karakter destekli lowercase tokenizer."""
    return _token_pattern.findall(text.lower())


def build_bm25_retriever(chunks: list[Document]) -> BM25Retriever:
    """Ingestion sırasında mevcut chunk'lar için hazır BM25Retriever oluşturur."""
    return BM25Retriever.from_documents(chunks, preprocess_func=_tokenize)


def save_bm25_retriever(chunks: list[Document]) -> None:
    """BM25 index'ini ingestion çıktısı olarak diske kaydeder."""
    retriever = build_bm25_retriever(chunks)
    _index_path.parent.mkdir(parents=True, exist_ok=True)
    with _index_path.open("wb") as index_file:
        pickle.dump(retriever, index_file)


def load_bm25_retriever() -> BM25Retriever:
    """Daha önce ingestion sırasında kaydedilmiş BM25 index'ini yükler."""
    if not _index_path.exists():
        raise FileNotFoundError(
            f"BM25 index bulunamadı: {_index_path}. "
            "Önce ingestion çalıştırılmalı."
        )

    with _index_path.open("rb") as index_file:
        return pickle.load(index_file)
