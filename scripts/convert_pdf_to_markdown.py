import argparse
from pathlib import Path

from src.rag.loaders.docling_loader import convert_pdf_to_markdown
from src.rag.normalizers.product_markdown_formatter import format_product_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a product PDF to normalized Markdown.")
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_markdown", type=Path)
    parser.add_argument("--product-id", required=True)
    parser.add_argument("--product-name", required=True)
    parser.add_argument("--source-type", required=True)
    parser.add_argument("--source-date")
    args = parser.parse_args()

    raw_markdown = convert_pdf_to_markdown(args.input_pdf)
    normalized = format_product_markdown(
        raw_markdown,
        product_id=args.product_id,
        product_name=args.product_name,
        source_type=args.source_type,
        source_file=args.input_pdf.name,
        source_date=args.source_date,
    )

    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.write_text(normalized, encoding="utf-8")
    print(f"Markdown oluşturuldu: {args.output_markdown}")
    print(f"Karakter sayısı: {len(normalized)}")


if __name__ == "__main__":
    main()
