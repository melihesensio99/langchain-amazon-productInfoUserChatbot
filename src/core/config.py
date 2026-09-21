from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Amazon Product RAG API"
    mistral_api_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "amazon_products"
    embedding_model: str = "intfloat/multilingual-e5-small"
    embedding_device: str = "cpu"
    top_k: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
