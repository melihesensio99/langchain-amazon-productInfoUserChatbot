from fastapi import APIRouter

from src.schemas.ingest import IngestResponse
from src.services.ingestion_service import IngestionService

router = APIRouter()


@router.post("", response_model=IngestResponse)
def ingest() -> IngestResponse:
    count = IngestionService().ingest_csv()
    return IngestResponse(indexed_documents=count)
