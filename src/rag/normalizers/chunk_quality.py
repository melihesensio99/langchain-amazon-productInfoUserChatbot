import re
from dataclasses import dataclass

from langchain_core.documents import Document


_LINK_PATTERN = re.compile(r"https?://|\]\(")
_CONTEXT_PREFIX = re.compile(r"^\[Belge:[^\n]+\]\s*")
_NAVIGATION_TERMS = (
    "site haritası",
    "kullanım şartları",
    "gizlilik politikası",
    "privacy policy",
    "terms of use",
    "sitemap",
)


@dataclass(frozen=True)
# PROJEYE ÖZEL RAPOR SINIFI: Chunk kalite ölçümlerini ve filtreleme kararını
# taşır.
class ChunkQualityReport:
    """Bir chunk'ın kalite ölçümlerini ve filtreleme kararını taşır."""

    # Chunk'ın temel kalite ölçümleri.
    characters: int
    words: int
    links: int
    boilerplate_score: int

    # Skorun nedenlerini açıklar.
    reasons: tuple[str, ...]

    @property
    def should_filter(self) -> bool:
        return self.boilerplate_score >= 3 or "heading_only" in self.reasons


def analyze_chunk(document: Document) -> ChunkQualityReport:
    text = document.page_content.strip()
    # Breadcrumb kalite hesabını etkilemesin; yalnızca gerçek içerik ölçülür.
    analysis_text = _CONTEXT_PREFIX.sub("", text, count=1).strip()
    words = len(analysis_text.split())
    links = len(_LINK_PATTERN.findall(analysis_text))
    score = 0
    reasons: list[str] = []

    if words < 30:
        # Çok kısa içerikler footer veya yalnızca başlık olabilir.
        score += 1
        reasons.append("short_text")

    if links >= 2:
        # Kısa ve çok linkli içerikler genellikle navigasyon/footer'dır.
        score += 2
        reasons.append("multiple_links")
    elif links == 1 and words < 20:
        score += 1
        reasons.append("short_link_text")

    lowered = analysis_text.casefold()
    if any(term in lowered for term in _NAVIGATION_TERMS):
        # Site haritası ve kullanım şartları gibi ürün dışı metinleri işaretler.
        score += 2
        reasons.append("navigation_language")

    is_single_heading = (
        analysis_text.startswith("#")
        and len(analysis_text.splitlines()) <= 1
    )
    contains_structured_value = ":" in analysis_text or any(
        char.isdigit() for char in analysis_text
    )
    if is_single_heading and not contains_structured_value:
        # Sadece başlık olan chunk embedding için anlamlı içerik taşımaz.
        score += 1
        reasons.append("heading_only")

    return ChunkQualityReport(
        characters=len(analysis_text),
        words=words,
        links=links,
        boilerplate_score=score,
        reasons=tuple(reasons),
    )
