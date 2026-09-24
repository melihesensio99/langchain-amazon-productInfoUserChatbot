"""Convert every PDF described by a document manifest to processed Markdown."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from src.rag.loaders.docling_loader import convert_pdf_to_markdown
from src.rag.normalizers.product_markdown_formatter import format_product_markdown


def convert_manifest(manifest_path: str | Path) -> int:
    manifest_file = Path(manifest_path)
    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
    source_dir = Path(manifest["source_dir"])
    output_dir = Path(manifest.get("output_dir", "data/processed"))
    raw_dir = Path(manifest.get("raw_dir", "data/raw"))
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    documents = manifest.get("documents", [])
    if not documents:
        raise ValueError("Manifest içinde en az bir documents kaydı olmalı.")

    for item in documents:
        pdf_path = source_dir / Path(item["file"])
        if not pdf_path.exists():
            raise FileNotFoundError(f"Manifest PDF'i bulunamadı: {pdf_path}")

        metadata = dict(item)
        metadata.pop("file")
        output_name = metadata.pop("output", f"{pdf_path.stem}.md")
        raw_name = metadata.pop("raw_output", f"{pdf_path.stem}-raw.md")

        required = ["product_id", "product_name", "source_type"]
        missing = [key for key in required if not metadata.get(key)]
        if missing:
            raise ValueError(f"{pdf_path.name} için eksik alanlar: {missing}")

        product_id = metadata.pop("product_id")
        product_name = metadata.pop("product_name")
        source_type = metadata.pop("source_type")
        source_date = metadata.pop("source_date", None)

        print(f"Dönüştürülüyor: {pdf_path.name}")
        raw_markdown = convert_pdf_to_markdown(pdf_path)
        (raw_dir / raw_name).write_text(raw_markdown, encoding="utf-8")
        normalized = format_product_markdown(
            raw_markdown,
            product_id=product_id,
            product_name=product_name,
            source_type=source_type,
            source_file=pdf_path.name,
            source_date=source_date,
            extra_metadata=metadata,
        )
        output_path = output_dir / output_name
        output_path.write_text(normalized, encoding="utf-8")
        print(f"  Markdown: {output_path}")

    return len(documents)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manifest'teki PDF'leri Markdown'a dönüştür.")
    parser.add_argument(
        "manifest",
        type=Path,
        nargs="?",
        default=Path("data/document_manifest.yaml"),
    )
    args = parser.parse_args()
    count = convert_manifest(args.manifest)
    print(f"Tamamlandı: {count} PDF işlendi.")


if __name__ == "__main__":
    main()
