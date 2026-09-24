import html
import re


_IMAGE_COMMENT = re.compile(r"<!--\s*image\s*-->", flags=re.IGNORECASE)
_HEADING_FOOTNOTE = re.compile(r"^(#{1,6}\s+.*?)(?:\s+[1-9])\s*$")
_INLINE_LIST_MARKER = re.compile(r"(?<!\n)\s+([a-d])\.\s+(?=[A-ZÇĞİÖŞÜ])")
_TOC_MARKER = re.compile(
    r"^\s*(?:#+\s*)?(?:İÇERİK|İÇİNDEKİLER|TABLE OF CONTENTS|CONTENTS)\s*$",
    flags=re.IGNORECASE,
)
_TOC_ROW = re.compile(
    r"^\s*\|.*(?:\.{3,}|…{2,}).*\|\s*\d{1,3}\s*\|?\s*$"
)
_TOC_TABLE_TITLE = re.compile(
    r"(?:İÇİNDEKİLER|TABLE OF CONTENTS|CONTENTS)", flags=re.IGNORECASE
)
_FIELD_LABEL = r"[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü()/-]*(?:\s+[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü()/-]*){0,2}"
_STRUCTURED_FIELD = re.compile(
    rf"({_FIELD_LABEL})\s*:\s*(.*?)(?=\s+{_FIELD_LABEL}\s*:|$)"
)
_HEADING_TRAILING_RULE = re.compile(r"(?:\\_|_){3,}\s*$")
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")
_REPLACEMENT_CHARACTER = re.compile(r"(?:�|ï¿½)")
_WORD_WITH_SPACE = re.compile(r"(?P<left>[^\W\d_]+)(?P<space>[ \t]+)(?P<right>[^\W\d_]+)")
_LINK_ONLY = re.compile(r"^\s*\[([^\]]+)\]\([^)]*\)\s*$")
_TURKISH_MOJIBAKE = {
    # Bazı eski PDF çıktılarında Türkçe karakterler Windows kod sayfası
    # kalıntıları olarak gelir. Yalnızca iki harf arasında görüldüğünde
    # düzeltiriz; böylece gerçek para birimi/işaret karakterlerine dokunmayız.
    "€": "ğ",
    "›": "ı",
}


def _normalize_technical_heading(
    line: str,
    cleaned_lines: list[str],
) -> list[str]:
    """Teknik değerleri yanlışlıkla h2 olan Docling satırını normalleştirir."""
    match = re.match(r"^##\s+(.+)$", line)
    if not match:
        return [line]

    # Kategoriye özel alan adları kullanmayız. Bu kural; telefon, ayakkabı,
    # mobilya veya başka bir ürünün `Renk: ... Beden: ...` satırlarında da
    # çalışabilsin diye genel label:value biçimini algılar.
    fields = list(_STRUCTURED_FIELD.finditer(match.group(1)))
    if len(fields) < 2:
        return [line]

    # Docling çoğu zaman hemen önce doğru bir bölüm başlığı üretir; yoksa
    # kategori bağımsız genel bir başlık ekleriz.
    if not any(item.startswith("## ") for item in cleaned_lines[-3:]):
        cleaned_lines.append("## Özellikler")

    normalized_fields = []
    for field in fields:
        value = re.sub(r"\s+,", ",", field.group(2).strip())
        normalized_fields.append(f"- {field.group(1)}: {value}")
    return normalized_fields


def _remove_table_of_contents(lines: list[str]) -> list[str]:
    """Remove generic table-of-contents blocks from parser output.

    TOC blocks are navigation data, not product facts. The rule relies on the
    explicit TOC marker and the next Markdown heading, so it is not tied to a
    product category or a particular manual layout.
    """
    cleaned: list[str] = []
    skipping = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if not skipping and _TOC_MARKER.match(line.strip()):
            skipping = True
            index += 1
            continue
        if skipping:
            if re.match(r"^#{1,6}\s+", line.strip()):
                skipping = False
                cleaned.append(line)
            index += 1
            continue

        # Bazı Docling çıktılarında "İçindekiler" başlığı kaybolur. Bu
        # durumda tabloyu ürün kategorisine göre değil, genel biçimine göre
        # tanırız: satırlarda noktalı lider ve son hücrede sayfa numarası.
        # En az üç ardışık satır olması, normal teknik tabloları yanlışlıkla
        # silme riskini azaltır.
        if _TOC_ROW.match(line):
            end = index
            toc_rows = 0
            while end < len(lines) and lines[end].strip().startswith("|"):
                if _TOC_ROW.match(lines[end]):
                    toc_rows += 1
                end += 1
            if toc_rows >= 3:
                index = end
                continue

        # Bazı belgelerde içindekiler başlığı, tablonun ilk hücresine gömülür
        # (ör. `| İÇİNDEKİLER |`). Noktalı lider olmayan bu biçimi de yalnızca
        # aynı tablo bloğunda başlık açıkça geçtiğinde kaldırırız.
        if line.strip().startswith("|"):
            end = index
            table_lines: list[str] = []
            while end < len(lines) and lines[end].strip().startswith("|"):
                table_lines.append(lines[end])
                end += 1
            table_text = "\n".join(table_lines)
            if _TOC_TABLE_TITLE.search(table_text):
                index = end
                continue

        cleaned.append(line)
        index += 1
    return cleaned


def _looks_like_field_value_block(lines: list[str], heading_index: int) -> bool:
    """Bir başlığın altında art arda teknik alan/değer satırları var mı bakar."""
    following = [line.strip() for line in lines[heading_index + 1 :] if line.strip()][:6]
    if len(following) < 4:
        return False

    pairs = 0
    for index in range(0, len(following) - 1, 2):
        field, value = following[index : index + 2]
        if (
            not field.startswith(("#", "|", "-", "["))
            and len(field) <= 100
            and bool(re.search(r"\d|%|Hz|mm|MP|GB|TB|GHz|x\s", value, flags=re.I))
        ):
            pairs += 1
    return pairs >= 2


def _repair_linked_section_headings(lines: list[str]) -> list[str]:
    """Link etiketi ile yanlış eşleşmiş Docling bölüm başlıklarını düzeltir.

    Bazı PDF'lerde bölüm etiketi link olarak çıkarılır, sonraki gerçek teknik
    alanlar ise bir önceki/yanlış `##` başlığı altında görünür. Yalnızca altında
    en az iki alan/değer çifti bulunan bloklarda düzeltme yaparak normal linkleri
    ve sıradan başlıkları koruruz.
    """
    repaired = list(lines)
    for index, line in enumerate(lines):
        match = _LINK_ONLY.match(line.strip())
        if not match:
            continue

        heading_index = index + 1
        while heading_index < len(lines) and not lines[heading_index].strip():
            heading_index += 1
        if heading_index >= len(lines) or not re.match(r"^##\s+", lines[heading_index]):
            continue
        if not _looks_like_field_value_block(lines, heading_index):
            continue

        repaired[index] = f"## {match.group(1).strip()}"
        repaired[heading_index] = ""

    return repaired


def _repair_document_word_splits(text: str) -> str:
    """Belge içi sözlük kanıtıyla OCR kaynaklı kelime bölünmelerini birleştirir.

    Docling bazen `S mart`, `Switc h` veya `Displ ay` gibi parçalar üretir.
    Sabit ürün/marka sözlüğü kullanmak yerine, birleşik kelimenin aynı belgede
    başka bir yerde zaten geçtiğini kanıt olarak kullanıyoruz. Böylece farklı
    ürün ve dillerde rastgele kelimeleri birleştirme riski düşük tutulur.
    """
    vocabulary = {
        match.group(0).casefold()
        for match in re.finditer(r"[^\W\d_]+", text, flags=re.UNICODE)
    }

    def repair_line(line: str) -> str:
        for _ in range(2):
            changed = False

            def replace(match: re.Match[str]) -> str:
                nonlocal changed
                left = match.group("left")
                right = match.group("right")
                combined = f"{left}{right}"
                if (
                    len(combined) >= 5
                    and min(len(left), len(right)) <= 3
                    and combined.casefold() in vocabulary
                ):
                    changed = True
                    return combined
                return match.group(0)

            line = _WORD_WITH_SPACE.sub(replace, line)
            if not changed:
                break
        return line

    return "\n".join(repair_line(line) for line in text.splitlines())


def clean_docling_markdown(markdown: str) -> str:
    """Apply conservative, source-preserving cleanup to Docling Markdown."""
    text = html.unescape(markdown.replace("\u00a0", " "))
    text = _CONTROL_CHARACTERS.sub(" ", text)
    # PDF/parser'ın “karakter bilinmiyor” işaretini embedding'e taşımayız;
    # bu karakter geri kazanılamadığı için yalnızca boşlukla değiştirilebilir.
    text = _REPLACEMENT_CHARACTER.sub(" ", text)
    for broken, corrected in _TURKISH_MOJIBAKE.items():
        text = re.sub(
            rf"(?<=\w){re.escape(broken)}(?=\w|\s|[.,;:!?)]|$)",
            corrected,
            text,
        )
    text = _IMAGE_COMMENT.sub("", text)

    cleaned_lines: list[str] = []
    source_lines = _remove_table_of_contents(text.splitlines())
    source_lines = _repair_linked_section_headings(source_lines)
    for line in source_lines:
        stripped = line.rstrip()
        # Docling bazı PDF çizgilerini başlığın parçası gibi üretir.
        # Bu dekoratif çizgiler bölüm adının embedding'ini kirletmesin.
        if stripped.startswith("#"):
            stripped = _HEADING_TRAILING_RULE.sub("", stripped).rstrip()
        heading_match = _HEADING_FOOTNOTE.match(stripped)
        if heading_match:
            stripped = heading_match.group(1).rstrip()
        cleaned_lines.extend(_normalize_technical_heading(stripped, cleaned_lines))

    text = "\n".join(cleaned_lines)
    text = _INLINE_LIST_MARKER.sub(lambda match: f"\n- {match.group(1)}. ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = _repair_document_word_splits(text)
    return text.strip()
