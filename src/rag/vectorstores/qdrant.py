import os
from functools import lru_cache
from pathlib import Path

_project_root = Path(__file__).resolve().parents[3]
os.environ.setdefault("HF_HOME", str(_project_root / ".cache" / "huggingface"))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from src.core.config import get_settings


class E5Embeddings(HuggingFaceEmbeddings):
    """E5 modeli için doküman ve kullanıcı sorgusu prefix'lerini uygular."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # `passage:` prefix'i multilingual-e5 ailesinin önerdiği özel kullanım
        # biçimidir; model bunun bir aranacak doküman olduğunu anlar.
        prefixed_texts = [f"passage: {text}" for text in texts]
        return super().embed_documents(prefixed_texts)

    def embed_query(self, text: str) -> list[float]:
        # `query:` prefix'i de E5'e özeldir; model bunun kullanıcı araması
        # olduğunu belirtir ve passage vektörleriyle daha doğru eşleştirir.
        return super().embed_query(f"query: {text}")


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    settings = get_settings()
    # Prefix kullanımı her embedding modelinin genel kuralı değildir.
    # Burada aktif modelimiz multilingual-e5-small olduğu için uygulanır.
    return E5Embeddings(
        model_name=settings.embedding_model,
        cache_folder=str(_project_root / ".cache" / "huggingface"),
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": True},
    )


@lru_cache
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=get_settings().qdrant_url)


def ensure_collection() -> None:
    client = get_qdrant_client()
    collection_name = get_settings().qdrant_collection
    if client.collection_exists(collection_name):
        return

    vector_size = len(get_embeddings().embed_query("collection dimension probe"))
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )


def get_vector_store() -> QdrantVectorStore:
    settings = get_settings()
    ensure_collection()
    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=settings.qdrant_collection,
        embedding=get_embeddings(),
    )
