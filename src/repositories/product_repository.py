from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import Product, Review


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, product_id: str) -> Product | None:
        return self.db.get(Product, product_id)

    def list(self, skip: int, limit: int) -> list[Product]:
        return list(self.db.scalars(select(Product).order_by(Product.created_at.desc()).offset(skip).limit(limit)))

    def add(self, product: Product) -> Product:
        self.db.add(product)
        self.db.flush()
        return product

    def add_review(self, review: Review) -> Review:
        self.db.add(review)
        self.db.flush()
        return review
