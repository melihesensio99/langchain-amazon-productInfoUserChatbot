import asyncio
import json
import logging

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from src.core.config import get_settings
from src.db.session import SessionLocal
from src.messaging.rabbitmq import ProductIngestionJob
from src.repositories.product_repository import ProductRepository
from src.services.ingestion_service import IngestionService

logger = logging.getLogger(__name__)


class ProductIngestionConsumer:
    """RabbitMQ BackgroundService karşılığı: ürün ingestion job'larını tüketir."""

    max_retries = 3

    async def start(self) -> None:
        settings = get_settings()
        connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        try:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)
            queue = await channel.declare_queue(settings.rabbitmq_ingestion_queue, durable=True)

            logger.info("Consumer başladı: queue=%s", queue.name)
            async with queue.iterator() as messages:
                async for message in messages:
                    await self._handle_message(channel, queue.name, message)
        finally:
            await connection.close()

    async def _handle_message(self, channel, queue_name: str, message: AbstractIncomingMessage) -> None:
        try:
            payload = json.loads(message.body.decode("utf-8"))
            # Eski mesajlarda ek alanlar kalsa bile yalnızca correlation key'i kullanırız.
            job = ProductIngestionJob(product_id=payload["product_id"])
            with SessionLocal() as db:
                product = ProductRepository(db).get(job.product_id)
            if product is None:
                raise ValueError(f"Product bulunamadı: {job.product_id}")

            logger.info("Ingestion başladı: product_id=%s", job.product_id)
            chunks = await asyncio.to_thread(
                IngestionService().ingest_product_pdf,
                product_id=product.id,
                product_name=product.name,
                pdf_path=product.pdf_path,
            )
            await message.ack()
            logger.info("Ingestion tamamlandı: product_id=%s chunks=%s", job.product_id, chunks)
        except Exception:
            retry_count = int((message.headers or {}).get("x-retry-count", 0))
            if retry_count < self.max_retries:
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=message.body,
                        headers={"x-retry-count": retry_count + 1},
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=queue_name,
                )
                logger.exception("Ingestion başarısız, retry=%s", retry_count + 1)
            else:
                logger.exception("Ingestion %s retry sonrası başarısız oldu", self.max_retries)
            await message.ack()
