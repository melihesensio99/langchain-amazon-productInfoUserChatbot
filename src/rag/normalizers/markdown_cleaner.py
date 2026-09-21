import html
import re


_IMAGE_COMMENT = re.compile(r"<!--\s*image\s*-->", flags=re.IGNORECASE)
_HEADING_FOOTNOTE = re.compile(r"^(#{1,6}\s+.*?)(?:\s+[1-9])\s*$")
_INLINE_LIST_MARKER = re.compile(r"(?<!\n)\s+([a-d])\.\s+(?=[A-ZÇĞİÖŞÜ])")


def clean_docling_markdown(markdown: str) -> str:
    """Apply conservative, source-preserving cleanup to Docling Markdown."""
    text = html.unescape(markdown.replace("\u00a0", " "))
    text = _IMAGE_COMMENT.sub("", text)

    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.rstrip()
        heading_match = _HEADING_FOOTNOTE.match(stripped)
        if heading_match:
            stripped = heading_match.group(1).rstrip()
        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)
    text = _INLINE_LIST_MARKER.sub(lambda match: f"\n- {match.group(1)}. ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
