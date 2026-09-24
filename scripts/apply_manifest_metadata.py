"""Apply manifest metadata to already-generated raw Markdown files."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from src.rag.normalizers.product_markdown_formatter import format_product_markdown


def apply_manifest_metadata(manifest_path: str | Path) -> int:
    manifest_file = Path(manifest_path)
    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
    raw_dir = Path(manifest.get("raw_dir", "data/raw"))
    output_dir = Path(manifest.get("output_dir", "data/processed"))
    output_dir.mkdir(parents=True, exist_ok=True)

    for item in manifest["documents"]:
        pdf_name = Path(item["file"]).name
        raw_name = item.get("raw_output", f"{Path(pdf_name).stem}-raw.md")
        raw_path = raw_dir / raw_name
        if not raw_path.exists():
            raise FileNotFoundError(f"Ham Markdown bulunamadı: {raw_path}")

        metadata = dict(item)
        metadata.pop("file")
        output_name = metadata.pop("output", f"{Path(pdf_name).stem}.md")
        metadata.pop("raw_output", None)
        product_id = metadata.pop("product_id")
        product_name = metadata.pop("product_name")
        source_type = metadata.pop("source_type")
        source_date = metadata.pop("source_date", None)

        normalized = format_product_markdown(
            raw_path.read_text(encoding="utf-8"),
            product_id=product_id,
            product_name=product_name,
            source_type=source_type,
            source_file=pdf_name,
            source_date=source_date,
            extra_metadata=metadata,
        )
        (output_dir / output_name).write_text(normalized, encoding="utf-8")
        print(f"Metadata uygulandı: {output_dir / output_name}")

    return len(manifest["documents"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Manifest metadata'sını raw Markdown'lara uygula.")
    parser.add_argument("manifest", type=Path, nargs="?", default=Path("data/document_manifest.yaml"))
    args = parser.parse_args()
    print(f"Tamamlandı: {apply_manifest_metadata(args.manifest)} Markdown güncellendi.")


if __name__ == "__main__":
    main()
