import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Response, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.core.config import get_settings
from src.messaging.rabbitmq import ProductIngestionJob, RabbitMQPublisher
from src.schemas.product import (
    ProductCreate,
    ProductQueuedResponse,
    ProductResponse,
    ProductUpdate,
    ReviewCreate,
    ReviewResponse,
)
from src.services.product_service import ProductAlreadyExistsError, ProductNotFoundError, ProductService

router = APIRouter()


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


def _save_upload(upload: UploadFile, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as destination:
        shutil.copyfileobj(upload.file, destination)


@router.post("", response_model=ProductQueuedResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_product(
    product_id: str | None = Form(default=None, min_length=1, max_length=120),
    name: str = Form(..., min_length=1, max_length=255),
    pdf: UploadFile = File(...),
    service: ProductService = Depends(get_product_service),
) -> ProductQueuedResponse:
    if Path(pdf.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(status_code=415, detail="Only PDF uploads are supported.")

    settings = get_settings()
    relative_path = Path(settings.upload_dir) / f"{uuid4().hex}.pdf"
    absolute_path = relative_path.resolve()
    await run_in_threadpool(_save_upload, pdf, absolute_path)
    data = ProductCreate(id=product_id, name=name, pdf_path=str(relative_path))
    try:
        product = service.create(data)
    except ProductAlreadyExistsError as exc:
        absolute_path.unlink(missing_ok=True)
        raise HTTPException(status_code=409, detail=f"Product '{exc.args[0]}' already exists.") from exc

    try:
        await RabbitMQPublisher().publish_product_ingestion(
            ProductIngestionJob(product_id=product.id)
        )
    except Exception as exc:
        service.delete(product.id)
        absolute_path.unlink(missing_ok=True)
        raise HTTPException(status_code=503, detail="Ingestion queue is unavailable.") from exc

    return ProductQueuedResponse(product=product)


@router.get("", response_model=list[ProductResponse])
def list_products(
    skip: int = Query(default=0, ge=0), limit: int = Query(default=20, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    return service.list(skip, limit)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, service: ProductService = Depends(get_product_service)) -> ProductResponse:
    try:
        return service.get(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found.") from exc


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, data: ProductUpdate, service: ProductService = Depends(get_product_service)) -> ProductResponse:
    try:
        return service.update(product_id, data)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found.") from exc
    except ProductAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=f"SKU conflicts with another product.") from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, service: ProductService = Depends(get_product_service)) -> Response:
    try:
        service.delete(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found.") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{product_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(product_id: str, data: ReviewCreate, service: ProductService = Depends(get_product_service)) -> ReviewResponse:
    try:
        return service.add_review(product_id, data)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found.") from exc


@router.get("/{product_id}/reviews", response_model=list[ReviewResponse])
def list_reviews(product_id: str, service: ProductService = Depends(get_product_service)) -> list[ReviewResponse]:
    try:
        return service.get(product_id).reviews
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found.") from exc
