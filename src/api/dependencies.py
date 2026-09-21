from functools import lru_cache

from src.services.chat_service import ChatService


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()
