from functools import lru_cache

from langchain_mistralai import ChatMistralAI

from src.core.config import get_settings


@lru_cache
def get_llm() -> ChatMistralAI:
    settings = get_settings()
    return ChatMistralAI(
        # Mistral Ministral 3 8B API modeli; küçük ve hızlı generation için.
        model="ministral-8b-2512",
        temperature=0,
        api_key=settings.mistral_api_key,
    )
