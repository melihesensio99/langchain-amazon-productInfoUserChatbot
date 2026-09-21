from pathlib import Path

import pandas as pd
from langchain_core.documents import Document

from src.rag.loaders.markdown_loader import load_markdown_document, load_processed_markdown


def load_csv_documents(csv_path: str | Path) -> list[Document]:
    dataframe = pd.read_csv(csv_path, keep_default_na=False)
    documents: list[Document] = []

    for row in dataframe.to_dict(orient="records"):
        metadata = {
            key: row[key]
            for key in (
                "document_id", "urun_id", "urun_adi", "kategori", "icerik_turu",
                "baslik", "yazar", "kaynak_tipi", "puan", "dogrulanmis", "tarih",
            )
            if key in row and row[key] != ""
        }
        documents.append(Document(page_content=row["rag_metni"], metadata=metadata))

    return documents


def load_markdown_documents(markdown_path: str | Path) -> list[Document]:
    return [load_markdown_document(markdown_path)]
