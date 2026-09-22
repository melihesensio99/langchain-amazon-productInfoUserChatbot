from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat endpoint'ine gelen kullanıcı sorusunu temsil eder."""

    question: str = Field(min_length=2)


class ChatResponse(BaseModel):
    """Chat cevabını ve kullanılan kaynak bilgilerini temsil eder."""

    answer: str
    sources: list[dict] = Field(default_factory=list)
