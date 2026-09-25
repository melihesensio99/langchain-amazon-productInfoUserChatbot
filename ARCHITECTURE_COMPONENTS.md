# Mimari Bileşenleri

Bu dosya, mevcut kodda bizim yazdığımız proje bileşenleri ile LangChain ve diğer kütüphanelerden kullandığımız hazır bileşenleri ayırır.

## Güncel ana akış

```text
ChatRequest
    ↓
ChatService
    ↓
Product Retriever
    ├── QdrantVectorStore.as_retriever()  → semantic search
    └── BM25Retriever                     → keyword search
    ↓
merge_retrieval_candidates()
    ↓
context expansion
    ↓
CrossEncoder reranker
    ↓
top_k Document listesi
    ↓
QA chain + Mistral
    ↓
ChatResponse: answer + sources
```

Ana akışta RRF veya `EnsembleRetriever` kullanılmıyor. Semantic ve BM25 sonuçları ayrı ayrı alınır, duplicate'ler temizlenerek ortak aday havuzu oluşturulur ve bu adaylar reranker'a gönderilir. RRF yalnızca `src/rag/retrievers/debug/hybrid_retriever.py` içindeki manuel karşılaştırma aracında bulunur.

## Bizim yazdığımız proje bileşenleri

### `src/core/config.py`

`Settings`, Pydantic Settings'ten türeyen proje ayar sınıfıdır. Qdrant adresi, collection, embedding modeli, `top_k`, reranker ve retrieval ayarlarını `.env` ile birleştirir.

### `src/services/chat_service.py`

`ChatService`, API isteğini orkestre eder:

1. `product_id` ile product retriever'ı seçer.
2. Soruyu retrieval akışına gönderir.
3. Gelen Document listesini QA chain'e aktarır.
4. Kaynak metadata'sını `ChatResponse` içine koyar.

### `src/services/ingestion_service.py`

İşlenmiş Markdown dosyalarını yükler, chunk'lar ve Qdrant full sync işlemini başlatır. BM25 index'i de ingestion çıktısı olarak güncellenir.

### `src/rag/loaders/`

- `docling_loader.py`: PDF'i Docling ile ham Markdown'a dönüştürür.
- `markdown_loader.py`: Frontmatter metadata'sını ayırır ve LangChain `Document` oluşturur.
- `text_splitter.py`: Başlık ve tablo farkındalıklı chunking, breadcrumb context, duplicate temizliği ve kalite filtresi akışını yönetir.

### `src/rag/normalizers/`

- `markdown_cleaner.py`: Docling parser artıklarını, footer'ları, bozuk başlıkları ve yapısal gürültüyü temizler.
- `product_markdown_formatter.py`: Manifest metadata'sını Markdown frontmatter'ına ekler.
- `chunk_quality.py`: Chunk'ın indexlenmeye uygun olup olmadığını raporlar.

### `src/rag/vectorstores/qdrant.py`

`E5Embeddings`, `HuggingFaceEmbeddings` sınıfını ürün projesine uyarlar. E5 modeli için query ve passage prefix'lerini burada ekler. Aynı dosya Qdrant collection oluşturma, deterministic point ID ve full sync davranışını da yönetir.

### `src/rag/retrievers/product_retriever.py`

Ana production retriever akışıdır. Qdrant semantic retriever ile hazır LangChain BM25 retriever'ı paralel çalıştırır. Ürün sayfasından gelen `product_id`, Qdrant payload filtresine ve ürün bazlı BM25 chunk seçimine uygulanır.

### `src/rag/retrievers/context_expander.py`

Bulunan chunk'ın aynı bölümündeki ilişkili veya yakın chunk'ları aday havuzuna ekler. Özellikle bölünmüş teknik tablolar için bağlamı tamamlar.

### `src/rag/rerankers/cross_encoder.py`

`BAAI/bge-reranker-v2-m3` CrossEncoder'ını lazy-load eder. Semantic ve BM25'ten gelen adayları query-document ilgisine göre yeniden sıralar ve son `top_k` listesini döndürür.

### `src/rag/chains/qa_chain.py`

Retrieval'dan gelen Document'ları prompt context'ine çevirir, Mistral generation'ı çalıştırır ve model çıktısındaki Markdown işaretlerini temizler.

### `src/rag/retrievers/debug/`

Manuel gözlem ve karşılaştırma araçlarıdır; ana chatbot akışında kullanılmazlar:

| Dosya | Görevi |
|---|---|
| `qdrant_retriever.py` | Semantic skor ve metadata'yı doğrudan gösterir |
| `keyword_retriever.py` | Manuel BM25 sonuçlarını ve skorlarını gösterir |
| `hybrid_retriever.py` | Debug amaçlı semantic + BM25 + RRF karşılaştırması yapar |

## Hazır kütüphane bileşenleri

| Bileşen | Kütüphane | Kullanım |
|---|---|---|
| `BaseSettings` | Pydantic Settings | Environment ayarlarının temeli |
| `BaseModel` | Pydantic | API schema'larının temeli |
| `Document` | LangChain Core | `page_content` ve `metadata` taşıyan veri nesnesi |
| `ChatPromptTemplate` | LangChain Core | System ve human prompt şablonu |
| `RunnableParallel` | LangChain Core | Semantic ve BM25 kollarını paralel çalıştırır |
| `RunnableLambda` | LangChain Core | Python fonksiyonunu LCEL akışına bağlar |
| `StrOutputParser` | LangChain Core | LLM çıktısını string'e çevirir |
| `MarkdownHeaderTextSplitter` | LangChain Text Splitters | Markdown başlıklarına göre ilk bölme |
| `RecursiveCharacterTextSplitter` | LangChain Text Splitters | Gerekirse uzun içerikleri bölme |
| `HuggingFaceEmbeddings` | LangChain HuggingFace | Embedding model adaptörü |
| `QdrantVectorStore` | LangChain Qdrant | Qdrant ile LangChain entegrasyonu |
| `QdrantClient` | Qdrant Client | Qdrant API bağlantısı |
| `BM25Retriever` | LangChain Community | Hazır keyword retriever |
| `ChatMistralAI` | LangChain Mistral | Mistral API bağlantısı |
| `CrossEncoder` | Sentence Transformers | Reranking modeli |
| `DocumentConverter` | Docling | PDF → Markdown dönüşümü |
| `FastAPI`, `APIRouter` | FastAPI | HTTP API katmanı |

## BM25 indexleme nerede gerçekleşiyor?

BM25 index'i kullanıcı sorusu geldiğinde sıfırdan oluşturulmaz. Ingestion sırasında güncel chunk listesiyle oluşturulur ve `data/indexes/bm25_retriever.pkl` dosyasına kaydedilir.

```text
İşlenmiş Markdown
    ↓
Chunk listesi
    ↓
build_bm25_retriever()
    ↓
data/indexes/bm25_retriever.pkl
    ↓
load_bm25_retriever()
    ↓
Kullanıcı sorusunda keyword araması
```

Ürün sayfası için `product_id` verilirse mevcut chunk'lar o ürünle sınırlandırılarak ürün bazlı BM25 retriever oluşturulur.

## Main akış ile debug akışının farkı

### Main product retriever

```text
Qdrant semantic retriever
        +
LangChain BM25Retriever
        ↓
merge_retrieval_candidates()
        ↓
context expansion
        ↓
CrossEncoder reranker
```

Bu akışta RRF yoktur. İki retrieval kolunun adayları kaybolmasın diye ayrı ayrı korunur.

### Debug hybrid retriever

```text
Manuel Qdrant skorları
        +
Manuel BM25 skorları
        ↓
RRF
        ↓
Terminalde karşılaştırmalı sonuç
```

Bu akış yalnızca algoritmayı gözlemlemek ve A/B testi yapmak içindir.

## Güncel ürün bağlamı

Mevcut test ürünü:

```text
SecureHome SHL-500 Smart Lock
product_id: SECUREHOME-SHL-500
```

Önceki iPhone, Samsung, Grundig, MSI ve TV ürünleri güncel veri setinden çıkarılmıştır. Yeni ürünler eklendiğinde ingestion aynı genel akışla çalışır; ürün bilgileri manifestten, bölüm bilgileri Markdown başlıklarından gelir.
