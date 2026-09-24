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
    extra_metadata: dict[str, str] | None = None,
) -> str:
    """Wrap Docling Markdown in the stable product-document format."""
    cleaned = clean_docling_markdown(raw_markdown)
    if not cleaned:
        raise ValueError("Docling boş Markdown çıktısı üretti.")

    effective_date = source_date or date.today().isoformat()
    metadata = dict(extra_metadata or {})
    # Temel kimlik alanları formatter tarafından kanonik olarak belirlenir.
    metadata.update(
        {
            "product_id": product_id,
            "product_name": product_name,
            "source_type": source_type,
            "source_file": source_file,
            "source_date": effective_date,
        }
    )
    frontmatter = "\n".join(
        ["---"]
        + [f"{key}: {_yaml_value(str(value))}" for key, value in metadata.items()]
        + ["---"]
    )

    title = f"# {product_name}"
    if cleaned.startswith("# "):
        cleaned = cleaned.split("\n", 1)[1].lstrip() if "\n" in cleaned else ""

    return f"{frontmatter}\n\n{title}\n\n{cleaned}\n"
