import os
import uuid
from functools import lru_cache
from pathlib import Path

_project_root = Path(__file__).resolve().parents[3]
os.environ.setdefault("HF_HOME", str(_project_root / ".cache" / "huggingface"))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from src.core.config import get_settings


# PROJEYE ÖZEL ADAPTER SINIFI: E5 modeline ait query/passage prefix'lerini
# hazır HuggingFaceEmbeddings davranışının üzerine ekler.
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


def _chunk_id(document: Document) -> str:
    """Aynı içeriğe sabit, değişen içeriğe yeni UUID üretir."""
    metadata = document.metadata
    identity = "\n".join(
        [
            str(metadata.get("product_id", "")),
            str(metadata.get("source_file", "")),
            document.page_content,
        ]
    )
    return str(uuid.uuid5(uuid.NAMESPACE_URL, identity))


def sync_documents_to_qdrant(documents: list[Document]) -> int:
    """Güncel chunk kümesini Qdrant ile tam senkronize eder.

    PDF değişince chunk sınırları kayabilir. İçerik tabanlı ID'ler bu durumda
    değişen tüm chunk'ları yeni point olarak kabul eder; eski ID'ler stale
    kabul edilip silinir. Böylece güvenli full reindex gerçekleşir.
    """
    ensure_collection()
    client = get_qdrant_client()
    collection_name = get_settings().qdrant_collection

    document_ids = []
    for document in documents:
        # Aynı içerik tekrar işlendiğinde yeni point değil mevcut point güncellenir.
        document_id = _chunk_id(document)
        document.metadata["chunk_id"] = document_id
        document_ids.append(document_id)

    existing_ids: set[str] = set()
    offset = None
    while True:
        records, offset = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=False,
            with_vectors=False,
        )
        existing_ids.update(str(record.id) for record in records)
        if offset is None:
            break

    # Güncel Markdown klasörü source of truth'tur. Chunk sınırları kaydıysa
    # eski ID'ler desired_ids içinde bulunmaz ve stale olarak temizlenir.
    desired_ids = set(document_ids)
    stale_ids = existing_ids - desired_ids
    if stale_ids:
        # Artık processed Markdown'larda bulunmayan eski chunk'ları temizler.
        client.delete(
            collection_name=collection_name,
            points_selector=models.PointIdsList(points=list(stale_ids)),
        )

    # add_documents aynı ID varsa upsert eder, yoksa yeni point oluşturur.
    get_vector_store().add_documents(documents, ids=document_ids)
    return len(documents)
