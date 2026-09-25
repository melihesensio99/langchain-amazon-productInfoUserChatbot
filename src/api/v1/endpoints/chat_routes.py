import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies import get_chat_service
from src.db.session import get_db
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.services.product_service import ProductNotFoundError, ProductService

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    db: Session = Depends(get_db),
) -> ChatResponse:
    try:
        # Frontend yalnızca filtre anahtarını gönderir; ürünün gerçek kaynağı DB'dir.
        if request.product_id:
            ProductService(db).get(request.product_id)
        return service.answer(request)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found.") from exc
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
