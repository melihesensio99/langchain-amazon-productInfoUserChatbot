from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Uygulamanın environment ve varsayılan konfigürasyonunu taşır."""

    # API ve uygulama ayarları.
    app_name: str = "Amazon Product RAG API"
    mistral_api_key: str = ""

    # Qdrant bağlantı ve collection ayarları.
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "amazon_products"

    # Embedding modeli ve retrieval arama ayarları.
    # Lokal ve hafif embedding modeli; chunk ve query vektörlerini üretir.
    embedding_model: str = "intfloat/multilingual-e5-small"
    embedding_device: str = "cpu"
    # Qdrant'tan en fazla kaç aday chunk getirileceğini belirler.
    top_k: int = 5
    # Bu skorun altındaki zayıf benzerlik sonuçları retrieval'dan elenir.
    retrieval_score_threshold: float = 0.82

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
