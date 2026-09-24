from fastapi import APIRouter

from src.api.v1.endpoints import chat_routes, ingest_routes, retrieval_routes

api_router = APIRouter()
api_router.include_router(chat_routes.router, prefix="/chat", tags=["chat"])
api_router.include_router(ingest_routes.router, prefix="/ingest", tags=["ingest"])
api_router.include_router(
    retrieval_routes.router,
    prefix="/retrieval",
    tags=["retrieval"],
)
