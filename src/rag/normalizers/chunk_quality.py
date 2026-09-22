import re
from dataclasses import dataclass

from langchain_core.documents import Document


_LINK_PATTERN = re.compile(r"https?://|\]\(")
_NAVIGATION_TERMS = (
    "site haritası",
    "kullanım şartları",
    "gizlilik politikası",
    "privacy policy",
    "terms of use",
    "sitemap",
)


@dataclass(frozen=True)
class ChunkQualityReport:
    characters: int
    words: int
    links: int
    boilerplate_score: int
    reasons: tuple[str, ...]

    @property
    def is_boilerplate_candidate(self) -> bool:
        return self.boilerplate_score >= 3


def analyze_chunk(document: Document) -> ChunkQualityReport:
    text = document.page_content.strip()
    words = len(text.split())
    links = len(_LINK_PATTERN.findall(text))
    score = 0
    reasons: list[str] = []

    if words < 30:
        score += 1
        reasons.append("short_text")

    if links >= 2:
        score += 2
        reasons.append("multiple_links")
    elif links == 1 and words < 20:
        score += 1
        reasons.append("short_link_text")

    lowered = text.casefold()
    if any(term in lowered for term in _NAVIGATION_TERMS):
        score += 2
        reasons.append("navigation_language")

    if text.startswith("#") and len(text.splitlines()) <= 1:
        score += 1
        reasons.append("heading_only")

    return ChunkQualityReport(
        characters=len(text),
        words=words,
        links=links,
        boilerplate_score=score,
        reasons=tuple(reasons),
    )
