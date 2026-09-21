from pathlib import Path

from docling.document_converter import DocumentConverter


def convert_pdf_to_markdown(pdf_path: str | Path) -> str:
    """Convert a PDF to Docling's Markdown representation."""
    source = Path(pdf_path)
    if not source.exists():
        raise FileNotFoundError(f"PDF bulunamadı: {source}")

    converter = DocumentConverter()
    result = converter.convert(str(source))
    return result.document.export_to_markdown()
