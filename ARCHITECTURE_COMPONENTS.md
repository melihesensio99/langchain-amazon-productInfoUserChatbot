# Mimari Bileşenleri: Manuel ve Hazır Sınıflar

Bu dosya, projede bizim yazdığımız sınıflarla kütüphanelerden gelen hazır sınıfları ayırır.

## Bizim yazdığımız sınıflar

### `src/core/config.py`

```python
class Settings(BaseSettings)
```

Proje ayarlarını taşır: Qdrant URL'i, collection adı, embedding modeli, `top_k` ve skor eşiği.
`BaseSettings` sınıfı Pydantic kütüphanesinden hazır gelir; `Settings` bizim proje sınıfımızdır.

### `src/core/exceptions.py`

```python
class RagException(Exception)
class ConfigurationError(RagException)
```

Projeye özel hata sınıflarıdır.

### `src/services/ingestion_service.py`

```python
class IngestionService
```

Markdown dokümanlarını yükler, chunk'lar ve Qdrant'a indexler.

### `src/services/chat_service.py`

```python
class ChatService
```

Retriever ve QA chain'i kullanarak chatbot isteğini orkestre eder.

### `src/schemas/chat.py` ve `src/schemas/ingest.py`

```python
class ChatRequest(BaseModel)
class ChatResponse(BaseModel)
class IngestResponse(BaseModel)
```

API istek ve cevaplarının veri modelleridir. `BaseModel` hazır Pydantic sınıfıdır; bu DTO sınıfları bize aittir.

### `src/rag/normalizers/chunk_quality.py`

```python
class ChunkQualityReport
```

Chunk'ın kısa, heading-only veya boilerplate olup olmadığını raporlar.

### `src/rag/vectorstores/qdrant.py`

```python
class E5Embeddings(HuggingFaceEmbeddings)
```

E5 modeline özel `query:` ve `passage:` prefix'lerini ekleyen bizim adapter sınıfımızdır. Temel embedding davranışı hazır `HuggingFaceEmbeddings` sınıfından gelir.

### `src/rag/retrievers/hybrid_retriever.py`

```python
class HybridRetriever(BaseRetriever)
```

Semantic ve özel BM25 fonksiyonlarımızı RRF ile birleştiren manuel prototiptir. Test ve debug amacıyla tutulur; ana product retriever akışında kullanılmaz.

## Hazır kütüphane sınıfları

Projede doğrudan veya kalıtım yoluyla kullandığımız hazır bileşenler:

| Sınıf | Kütüphane | Kullanım amacı |
|---|---|---|
| `BaseSettings` | Pydantic Settings | Ortam ayarları |
| `BaseModel` | Pydantic | API schema temel sınıfı |
| `Document` | LangChain Core | `page_content` + `metadata` taşıyan chunk |
| `BaseRetriever` | LangChain Core | Retriever arayüzü |
| `ChatPromptTemplate` | LangChain Core | Prompt şablonu |
| `StrOutputParser` | LangChain Core | LLM çıktısını metne çevirme |
| `RecursiveCharacterTextSplitter` | LangChain Text Splitters | Uzun metni parçalara bölme |
| `MarkdownHeaderTextSplitter` | LangChain Text Splitters | Markdown başlıklarına göre bölme |
| `HuggingFaceEmbeddings` | LangChain HuggingFace | Embedding üretme |
| `QdrantVectorStore` | LangChain Qdrant | LangChain-Qdrant bağlantısı |
| `QdrantClient` | Qdrant Client | Qdrant API bağlantısı |
| `ChatMistralAI` | LangChain Mistral | Mistral LLM bağlantısı |
| `BM25Okapi` | `rank-bm25` | Manuel BM25 prototipi |
| `BM25Retriever` | LangChain Community | Hazır keyword retriever |
| `EnsembleRetriever` | LangChain Classic | Birden fazla retriever'ı rank fusion ile birleştirme |
| `RunnableLambda` | LangChain Core | Ensemble sonucunu final `top_k` ile sınırlama |
| `DocumentConverter` | Docling | PDF → Markdown/doküman dönüşümü |
| `FastAPI`, `APIRouter` | FastAPI | HTTP API katmanı |

## Ana akışta hangileri kullanılıyor?

Ana chatbot retrieval akışı:

```text
product_retriever.py
    ↓
QdrantVectorStore.as_retriever()
    ↓
BM25Retriever.from_documents()
    ↓
EnsembleRetriever
    ↓
RunnableLambda ile final top_k
```

Bu akışta semantic ve keyword retriever'lar hazır LangChain bileşenleriyle oluşturulur.

Manuel test akışları:

```text
qdrant_retriever.py
    → similarity_search_with_score()

keyword_retriever.py
    → BM25Okapi + manuel skorlar

hybrid_retriever.py
    → manuel semantic + BM25 + RRF
```

## Manuel hybrid ile hazır ensemble farkı

### Manuel `HybridRetriever`

```text
Qdrant semantic search
+
özel BM25 fonksiyonu
→ bizim yazdığımız RRF
→ Document + RRF skoru
```

Avantajları:

- Ham semantic ve BM25 skorlarını inceleyebiliriz.
- Tokenization ve tekilleştirme tamamen kontrolümüzdedir.
- Debug ve deney için uygundur.

### Hazır `EnsembleRetriever`

```text
Qdrant retriever
+
LangChain BM25Retriever
→ hazır rank fusion
→ Document listesi
```

Avantajları:

- LangChain `BaseRetriever` arayüzüne uygundur.
- Chain'e doğrudan bağlanır.
- Daha az özel kod ve daha kolay bakım sağlar.
- `weights=[0.7, 0.3]` ile semantic/keyword etkisi ayarlanabilir.

Hazır ensemble genellikle ham skorları dışarı vermez; sonuçları `Document` olarak döndürür. Bu nedenle manuel hybrid debug için, hazır ensemble ise ana chatbot akışı için tutulur.

## Aynı sorguyla yapılan karşılaştırma

Sorgu:

```text
iPhone 14 kapasite 128 GB
```

Manuel hybrid ve hazır `product_retriever` akışlarında ilk sonuç aynı çıktı:

```text
Kapasite
128 GB
256 GB
512 GB
```

İlk dört sonuç da aynıydı; beşinci sırada küçük bir sıralama farkı görüldü. Manuel versiyon RRF skorunu gösterirken hazır ensemble yalnızca `Document` döndürdü.
