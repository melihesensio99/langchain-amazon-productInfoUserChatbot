import httpx
from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_chat_service
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    try:
        return service.answer(request)
    except httpx.HTTPStatusError as exc:
        # Mistral 429 gibi upstream hatalarını frontend'e 500 yerine
        # açıklanabilir bir servis hatası olarak bildiririz.
        if exc.response.status_code == 429:
            raise HTTPException(
                status_code=503,
                detail="LLM rate limit reached. Please try again later.",
            ) from exc
        raise HTTPException(
            status_code=502,
            detail="LLM provider request failed.",
        ) from exc
