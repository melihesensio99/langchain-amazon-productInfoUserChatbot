from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=2)


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict] = Field(default_factory=list)
