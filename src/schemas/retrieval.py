from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    """Frontend retrieval testinde gelen soru ve seçili ürün bilgisidir."""

    question: str = Field(min_length=2)
    product_id: str | None = None


class RetrievalChunk(BaseModel):
    """Retrieval sonucunda frontend'e gösterilecek chunk bilgisidir."""

    page_content: str
    metadata: dict = Field(default_factory=dict)


class RetrievalResponse(BaseModel):
    """LLM generation yapılmadan dönen retrieval adaylarını taşır."""

    results: list[RetrievalChunk] = Field(default_factory=list)
