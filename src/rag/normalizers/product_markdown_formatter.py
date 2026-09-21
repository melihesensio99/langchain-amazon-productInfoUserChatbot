from datetime import date

from src.rag.normalizers.markdown_cleaner import clean_docling_markdown


def _yaml_value(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def format_product_markdown(
    raw_markdown: str,
    *,
    product_id: str,
    product_name: str,
    source_type: str,
    source_file: str,
    source_date: str | None = None,
) -> str:
    """Wrap Docling Markdown in the project's stable product-document format."""
    cleaned = clean_docling_markdown(raw_markdown)
    if not cleaned:
        raise ValueError("Docling boş Markdown çıktısı üretti.")

    effective_date = source_date or date.today().isoformat()
    frontmatter = "\n".join(
        [
            "---",
            f"product_id: {_yaml_value(product_id)}",
            f"product_name: {_yaml_value(product_name)}",
            f"source_type: {_yaml_value(source_type)}",
            f"source_file: {_yaml_value(source_file)}",
            f"source_date: {_yaml_value(effective_date)}",
            "---",
        ]
    )

    title = f"# {product_name}"
    if cleaned.startswith("# "):
        cleaned = cleaned.split("\n", 1)[1].lstrip() if "\n" in cleaned else ""

    return f"{frontmatter}\n\n{title}\n\n{cleaned}\n"
