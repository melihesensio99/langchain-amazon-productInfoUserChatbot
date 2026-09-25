"""Product ingestion consumer entrypoint."""

import asyncio
import logging

from src.workers.product_ingestion_consumer import ProductIngestionConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


if __name__ == "__main__":
    try:
        asyncio.run(ProductIngestionConsumer().start())
    except KeyboardInterrupt:
        pass
