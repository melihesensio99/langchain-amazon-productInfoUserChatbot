from pydantic import BaseModel


class IngestResponse(BaseModel):
    indexed_documents: int
