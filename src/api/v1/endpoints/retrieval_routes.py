from fastapi import APIRouter

from src.rag.retrievers.product_retriever import get_product_retriever
from src.schemas.retrieval import RetrievalChunk, RetrievalRequest, RetrievalResponse

router = APIRouter()


@router.post("", response_model=RetrievalResponse)
def retrieve(request: RetrievalRequest) -> RetrievalResponse:
    """Sadece retrieval çalıştırır; LLM generation çağırmaz."""

    retriever = get_product_retriever(request.product_id)
    documents = retriever.invoke(request.question)
    return RetrievalResponse(
        results=[
            RetrievalChunk(
                page_content=document.page_content,
                metadata=document.metadata,
            )
            for document in documents
        ]
    )
