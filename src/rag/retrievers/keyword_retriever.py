import re
from functools import lru_cache

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from src.rag.loaders.markdown_loader import load_processed_markdown
from src.rag.loaders.text_splitter import split_markdown_documents


_TOKEN_PATTERN = re.compile(r"[\wÇĞİÖŞÜçğıöşü]+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    """BM25 için metni küçük harfli kelime token'larına ayırır."""
    return _TOKEN_PATTERN.findall(text.lower())


@lru_cache
def _get_keyword_index() -> tuple[BM25Okapi, tuple[Document, ...]]:
    """İşlenmiş chunk'lar üzerinden bir kez BM25 index'i oluşturur."""
    documents = load_processed_markdown("data/processed")
    chunks = split_markdown_documents(documents)
    tokenized_chunks = [_tokenize(chunk.page_content) for chunk in chunks]
    return BM25Okapi(tokenized_chunks), tuple(chunks)


def search_keyword_chunks(
    query: str,
    *,
    top_k: int = 5,
) -> list[tuple[Document, float]]:
    """Sorgudaki kelimeleri BM25 ile chunk'larda arar ve skorlar."""
    bm25, chunks = _get_keyword_index()
    query_tokens = _tokenize(query)
    scores = bm25.get_scores(query_tokens)

    ranked_indexes = sorted(
        range(len(chunks)),
        key=lambda index: scores[index],
        reverse=True,
    )

    # BM25 skoru cosine similarity ile aynı ölçekte değildir.
    # Bu yüzden skorlar ileride hybrid birleşimde doğrudan toplanmayacak;
    # önce normalize edilecek veya rank-based fusion uygulanacaktır.
    return [
        (chunks[index], float(scores[index]))
        for index in ranked_indexes[:top_k]
        if scores[index] > 0
    ]
