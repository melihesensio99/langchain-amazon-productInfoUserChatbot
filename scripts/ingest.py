from src.services.ingestion_service import IngestionService


if __name__ == "__main__":
    count = IngestionService().ingest_csv()
    print(f"Indexed chunks: {count}")
