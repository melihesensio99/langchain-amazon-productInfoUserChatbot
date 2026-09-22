from pydantic import BaseModel


class IngestResponse(BaseModel):
    """Ingestion sonucunda indexlenen chunk sayısını taşır."""

    indexed_documents: int
