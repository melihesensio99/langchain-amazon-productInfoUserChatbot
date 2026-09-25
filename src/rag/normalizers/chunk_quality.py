"""Structural quality checks for chunks created from Markdown documents.

The quality filter must be conservative: a short specification such as
``4K 60 Hz`` can be valuable, while a short navigation/footer block is not.
Therefore length is reported, but it is not enough by itself to discard a
chunk.  Filtering is based on structural evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from langchain_core.documents import Document


_CONTEXT_PREFIX = re.compile(r"^\[Belge:[^\n]+\]\s*", re.I)
_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\([^)]*\)")
_URL = re.compile(r"https?://\S+", re.I)
_TOC_DOT_LEADER = re.compile(r"(?:\.{5,}|…{3,})")
_HEADING = re.compile(r"^#{1,6}\s+\S+")
_IMAGE_PLACEHOLDER = re.compile(r"^\s*(?:<!--\s*(?:image|figure)\s*-->|\[image\])\s*$", re.I)
_NAVIGATION_HINTS = re.compile(
    r"(?:site\s+haritası|kullanım\s+şartları|gizlilik\s+politikası|"
    r"privacy\s+policy|terms\s+of\s+use|sitemap|table\s+of\s+contents)",
    re.I,
)


@dataclass(frozen=True)
class ChunkQualityReport:
    """Measured signals and the final filtering decision for one chunk."""

    characters: int
    words: int
    links: int
    boilerplate_score: int
    reasons: tuple[str, ...]

    @property
    def should_filter(self) -> bool:
        """Return true only when there is strong structural evidence."""

        hard_failures = {
            "empty",
            "heading_only",
            "image_only",
            "links_only",
            "table_of_contents_like",
        }
        return bool(hard_failures.intersection(self.reasons)) or (
            self.boilerplate_score >= 4
        )


def _analysis_text(document: Document) -> str:
    """Remove the generated breadcrumb before measuring chunk content."""

    return _CONTEXT_PREFIX.sub("", document.page_content.strip(), count=1).strip()


def _is_table(lines: list[str]) -> bool:
    """Recognize a Markdown table without interpreting its cell values."""

    table_lines = [line.strip() for line in lines if line.strip()]
    if len(table_lines) < 2:
        return False
    return "|" in table_lines[0] and bool(
        re.match(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$", table_lines[1])
    )


def analyze_chunk(document: Document) -> ChunkQualityReport:
    """Analyze a chunk using product-agnostic structural signals.

    A chunk is retained when it contains a table, a measurement, a list, or
    ordinary prose, even if it is short.  This avoids deleting valid product
    facts such as a single capacity or port specification.
    """

    text = _analysis_text(document)
    if not text:
        return ChunkQualityReport(0, 0, 0, 5, ("empty",))

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    links = len(_MARKDOWN_LINK.findall(text)) + len(_URL.findall(text))
    words = len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))
    reasons: list[str] = []
    score = 0

    if lines and all(_IMAGE_PLACEHOLDER.match(line) for line in lines):
        reasons.append("image_only")
        score += 5

    if lines and all(_HEADING.match(line) for line in lines):
        reasons.append("heading_only")
        score += 5

    if lines and all(_MARKDOWN_LINK.fullmatch(line) or _URL.fullmatch(line) for line in lines):
        reasons.append("links_only")
        score += 4

    if len(_TOC_DOT_LEADER.findall(text)) >= 2:
        reasons.append("table_of_contents_like")
        score += 5

    table = _is_table(lines)
    has_list = any(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line) for line in lines)
    has_value = bool(re.search(r"\d|%|\b(?:Hz|mm|cm|kg|g|GB|TB|V|W|MP)\b", text, re.I))

    # A table/list/value is evidence that a short chunk can still answer a
    # product question. Never mark it as short boilerplate solely by length.
    if words < 8 and not (table or has_list or has_value):
        reasons.append("short_text")

    if links >= 3:
        reasons.append("many_links")
        score += 2
    elif links and words <= 12 and not (table or has_value):
        reasons.append("link_heavy")
        score += 2

    if _NAVIGATION_HINTS.search(text) and words <= 40 and not has_value:
        reasons.append("navigation_language")
        score += 3

    return ChunkQualityReport(
        characters=len(text),
        words=words,
        links=links,
        boilerplate_score=score,
        reasons=tuple(dict.fromkeys(reasons)),
    )
