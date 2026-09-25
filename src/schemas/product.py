from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ReviewCreate(BaseModel):
    text: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)
    sentiment: Literal["positive", "negative", "neutral"] | None = None


class ReviewResponse(ReviewCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: str
    created_at: datetime


class ProductCreate(BaseModel):
    id: str | None = Field(default=None, min_length=1, max_length=120, description="Boş bırakılırsa backend UUID üretir")
    name: str = Field(min_length=1, max_length=255)
    pdf_path: str = Field(min_length=1)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    pdf_path: str | None = Field(default=None, min_length=1)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    pdf_path: str
    created_at: datetime
    updated_at: datetime
    reviews: list[ReviewResponse] = Field(default_factory=list)

    @computed_field
    @property
    def average_rating(self) -> float | None:
        if not self.reviews:
            return None
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 2)

    @computed_field
    @property
    def review_count(self) -> int:
        return len(self.reviews)


class ProductQueuedResponse(BaseModel):
    product: ProductResponse
    ingestion_status: Literal["queued"] = "queued"
