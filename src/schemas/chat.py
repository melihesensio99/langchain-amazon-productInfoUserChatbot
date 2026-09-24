from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat endpoint'ine gelen kullanıcı sorusunu temsil eder."""

    question: str = Field(min_length=2)
    # Ürün sayfası chatbot'u seçili ürünün ID'sini gönderir.
    # Genel arama ekranında bu alan boş bırakılabilir.
    product_id: str | None = None


class ChatResponse(BaseModel):
    """Chat cevabını ve kullanılan kaynak bilgilerini temsil eder."""

    answer: str
    sources: list[dict] = Field(default_factory=list)
