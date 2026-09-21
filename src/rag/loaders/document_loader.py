from pathlib import Path

import pandas as pd
from langchain_core.documents import Document


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
    path = Path(markdown_path)
    raw_text = path.read_text(encoding="utf-8")
    metadata: dict[str, str] = {"source_type": "markdown", "source_file": path.name}

    if raw_text.startswith("---"):
        _, frontmatter, content = raw_text.split("---", 2)
        for line in frontmatter.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
        raw_text = content.strip()

    return [Document(page_content=raw_text, metadata=metadata)]
