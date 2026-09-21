from src.services.ingestion_service import IngestionService


if __name__ == "__main__":
    count = IngestionService().ingest_processed_markdown()
    print(f"Indexed chunks: {count}")
