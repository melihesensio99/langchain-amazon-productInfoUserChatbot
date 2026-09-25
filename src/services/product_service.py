from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.models import Product, Review
from src.repositories.product_repository import ProductRepository
from src.schemas.product import ProductCreate, ProductUpdate, ReviewCreate


class ProductNotFoundError(Exception):
    pass


class ProductAlreadyExistsError(Exception):
    pass


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = ProductRepository(db)

    def create(self, data: ProductCreate) -> Product:
        if data.id and self.repository.get(data.id):
            raise ProductAlreadyExistsError(data.id)
        payload = data.model_dump(exclude_none=True)
        product = Product(**payload)
        try:
            self.repository.add(product)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ProductAlreadyExistsError(data.id) from exc
        self.db.refresh(product)
        return product

    def get(self, product_id: str) -> Product:
        product = self.repository.get(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    def list(self, skip: int, limit: int) -> list[Product]:
        return self.repository.list(skip, limit)

    def update(self, product_id: str, data: ProductUpdate) -> Product:
        product = self.get(product_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ProductAlreadyExistsError(product_id) from exc
        self.db.refresh(product)
        return product

    def delete(self, product_id: str) -> None:
        product = self.get(product_id)
        self.db.delete(product)
        self.db.commit()

    def add_review(self, product_id: str, data: ReviewCreate) -> Review:
        self.get(product_id)
        review = Review(product_id=product_id, **data.model_dump())
        self.repository.add_review(review)
        self.db.commit()
        self.db.refresh(review)
        return review
