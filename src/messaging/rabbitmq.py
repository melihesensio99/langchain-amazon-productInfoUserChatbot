import json
from dataclasses import asdict, dataclass

import aio_pika
from aio_pika import DeliveryMode, Message

from src.core.config import get_settings


@dataclass(frozen=True)
class ProductIngestionJob:
    product_id: str


class RabbitMQPublisher:
    """Publishes durable product-ingestion jobs to RabbitMQ."""

    async def publish_product_ingestion(self, job: ProductIngestionJob) -> None:
        settings = get_settings()
        connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        try:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)
            queue = await channel.declare_queue(settings.rabbitmq_ingestion_queue, durable=True)
            await channel.default_exchange.publish(
                Message(
                    body=json.dumps(asdict(job)).encode("utf-8"),
                    content_type="application/json",
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=queue.name,
            )
        finally:
            await connection.close()
