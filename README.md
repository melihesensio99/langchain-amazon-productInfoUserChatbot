# Product RAG Chatbot

Bu proje, e-ticaret ürünlerinin teknik dokümanlarını ve kullanım kılavuzlarını anlayarak ürün sayfası üzerinden kaynaklı cevaplar veren RAG tabanlı bir chatbot prototipidir.

Amaç yalnızca PDF'i embedding'e çevirip aramak değildir. Farklı kalitedeki PDF'leri temizleyen, anlamlı chunk'lara bölen, doğru ürüne göre filtreleyen, retrieval sonuçlarını yeniden sıralayan ve Mistral ile doğal cevap üreten sürdürülebilir bir pipeline oluşturuyoruz.

## Öne çıkan teknolojiler ve modeller

| Bileşen | Kullanılan teknoloji / model | Görevi |
|---|---|---|
| PDF parser | Docling | PDF'i yapısal Markdown'a dönüştürür |
| Orchestration | LangChain | Loader, splitter, retriever ve generation akışını birleştirir |
| Embedding | `intfloat/multilingual-e5-small` | Türkçe ve çok dilli metinleri vektörleştirir |
| Vector database | Qdrant | Chunk embedding'lerini ve metadata'yı saklar |
| Keyword search | BM25 | Exact terim, sayı ve model kodu eşleşmesi yapar |
| Reranker | `BAAI/bge-reranker-v2-m3` | Aday chunk'ları soruya göre yeniden sıralar |
| Generation LLM | Mistral `ministral-8b-2512` | Kaynak context'inden Türkçe cevap üretir |
| API | FastAPI | Ürün upload, chat ve yorum endpoint'lerini sunar |
| Frontend | React + Vite | Ürün ekranı ve chatbot arayüzünü sağlar |
| Relational database | PostgreSQL + SQLAlchemy | Ürün, PDF konumu ve yorum kayıtlarını tutar |
| Message broker | RabbitMQ + `aio-pika` | PDF ingestion job'larını kuyruğa alır |

## Projeyi gör

### Ürün dashboard'u

![SecureHome SHL-500 ürün dashboard'u](docs/screenshots/product-dashboard.png)

Ürün ekranında chatbot seçili ürünle birlikte açılır. Frontend, ürünün `product_id` değerini backend'e gönderir; böylece soru başka ürünlerin chunk'larıyla karışmaz.

### Kaynaklı cevaplar

![Kaynaklı teknik cevaplar](docs/screenshots/grounded-answers.png)

Pil bitmesi, ana montaj deliği ve vida seçimi sorularında cevapların altında kullanılan SecureHome SHL-500 dokümanı gösterilir.

### Kaynakta olmayan bilgiyi uydurmama

![Dokümanda olmayan DoorSense sorusu](docs/screenshots/missing-source-doorsense.png)

DoorSense bilgisi mevcut dokümanda olmadığı için chatbot tahmin üretmez ve bilginin belgede bulunmadığını belirtir.

![Dokümanda olmayan RAM ve işlemci sorusu](docs/screenshots/missing-source-specs.png)

RAM ve işlemci bilgisi kaynaklarda olmadığı için bu değerler icat edilmez. Sistem yalnızca belgede bulunan teknik özellikleri kullanır.

## Genel akış

### Ürün oluşturma ve asenkron ingestion

```text
Frontend / API multipart PDF upload
        ↓
PostgreSQL Product kaydı + UUID üretimi
        ↓
PDF data/uploads altına kaydedilir
        ↓
RabbitMQ product-ingestion queue
        ↓
ProductIngestionConsumer
        ↓
PDF katalog / kullanım kılavuzu
        ↓
Docling ile ham Markdown
        ↓
Markdown normalizasyonu + frontmatter metadata
        ↓
LangChain Markdown loader
        ↓
Başlık ve tablo farkındalıklı chunking
        ↓
Kalite filtresi + breadcrumb context
        ↓
multilingual-e5-small embedding
        ↓
Qdrant vector database
```

API PDF'i işlerken beklemez; `202 Accepted` ve `ingestion_status=queued` döndürür. Worker kapalıysa job RabbitMQ'da bekler.

### Sorudan cevaba

```text
Frontend sorusu + PostgreSQL'den alınmış product_id
        ↓
Backend ürünün PostgreSQL'de varlığını doğrular
        ↓
Semantic search + BM25 keyword search
        ↓
Duplicate temizleme + ortak aday havuzu
        ↓
Context expansion
        ↓
Cross-encoder reranker
        ↓
Mistral generation
        ↓
Cevap + kaynaklar
```

## Mimari

| Katman | Sorumluluk |
|---|---|
| `api` | FastAPI HTTP endpoint'leri |
| `schemas` | İstek ve cevap modelleri |
| `services` | Chat ve ingestion orkestrasyonu |
| `db` | SQLAlchemy modelleri ve PostgreSQL session yönetimi |
| `repositories` | Veritabanı erişim katmanı |
| `messaging` | RabbitMQ job publisher ve mesaj sözleşmeleri |
| `workers` | RabbitMQ consumer ve arka plan işleyicileri |
| `rag/loaders` | Docling, Markdown yükleme ve chunking |
| `rag/normalizers` | Parser artığı temizliği ve kalite kontrolü |
| `rag/retrievers` | Semantic, BM25, hybrid ve product retrieval |
| `rag/rerankers` | Aday chunk'ları yeniden sıralama |
| `rag/vectorstores` | Embedding ve Qdrant bağlantısı |
| `rag/prompts` | Generation prompt'ları |
| `frontend` | Ürün ekranı ve chatbot arayüzü |

## RAG kalitesini artırmak için yaptıklarımız

| İyileştirme | Faydası |
|---|---|
| Manifest metadata | Aynı ürüne ait farklı PDF'leri `product_id` altında toplar |
| Markdown normalizasyonu | Docling footer, placeholder, kontrol karakteri ve biçim artıklarını azaltır |
| Başlık farkındalıklı chunking | Teknik bilgi başlık ve tablo sınırlarında korunur |
| Breadcrumb context | Chunk'ın hangi ürün ve bölümden geldiğini embedding'e taşır |
| Chunk kalite filtresi | Boş, başlık-only ve düşük bilgi yoğunluklu chunk'ları eler |
| Hybrid retrieval | Semantic benzerlik ile exact keyword eşleşmesini birleştirir |
| Context expansion | Bölünmüş tablo ve yakın bölüm bağlamını tamamlar |
| Reranking | En uygun aday chunk'ı üst sıraya taşır |
| Deterministic chunk ID | Tekrar ingestion sırasında duplicate point oluşmasını önler |
| Kaynak kontrollü generation | Mistral'ın doküman dışı bilgi uydurmasını azaltır |

Normalizer bilinmeyen bir ürünün içeriğini elle yeniden yazmaz; genel yapısal temizlik uygular. Bu yüzden farklı ürün türleri için de kullanılabilir.

## Ürün, yorum ve metadata modeli

Ürün tablosu bilinçli olarak minimal tutulur:

```text
Product
├── id          UUID (backend üretir)
├── name
├── pdf_path
├── created_at
└── updated_at
```

Yorum tablosu:

```text
Review
├── id
├── product_id
├── text
├── rating
├── sentiment   positive | negative | neutral | null
└── created_at
```

PDF Markdown'a dönüştürülürken RAG metadata'sı PostgreSQL Product kaydından oluşturulur:

```text
Product.id → metadata.product_id
Product.name → metadata.product_name
Product.pdf_path → metadata.source_file
```

## Mevcut test akışı

Test için SecureHome SHL-500 PDF'i upload endpointi üzerinden gönderilebilir. Ürün ID'si elle verilmez; response içindeki `product.id` backend tarafından üretilir ve chat isteğinde kullanılır.

## Kurulum

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`.env` dosyasına Mistral API anahtarını ekleyin. API anahtarını Git'e commit etmeyin.

Qdrant, PostgreSQL ve RabbitMQ:

```powershell
docker compose up -d qdrant postgres rabbitmq
```

Dashboard: <http://localhost:6333/dashboard>

Veritabanı tablolarını migration ile oluşturun:

```powershell
.venv\Scripts\python.exe -m alembic upgrade head
```

## Eski manifest tabanlı ingestion

Manifest scriptleri toplu/legacy ingestion için hâlâ kullanılabilir:

```powershell
.venv\Scripts\python.exe -m scripts.convert_manifest data\document_manifest.yaml
.venv\Scripts\python.exe -m scripts.ingest
.venv\Scripts\python.exe -m scripts.inspect_chunks
```

## Backend ve frontend

Backend:

```powershell
.venv\Scripts\python.exe -m uvicorn src.main:app --reload --port 8000
```

Yerel Python geliştirme akışında API ve worker ayrı process olarak çalıştırılabilir:

```powershell
.venv\Scripts\python.exe -m scripts.rag_worker
```

Ürün oluşturma endpoint'i `multipart/form-data` kabul eder:

```text
POST /api/v1/products
name: SecureHome SHL-500
pdf: <manual.pdf>
```

`product_id` gönderilmezse backend UUID üretir. Upload response'undaki `product.id`, sonraki chat isteğinde `product_id` olarak kullanılır.

API PDF'i `data/uploads` altına kaydeder, ürünü PostgreSQL'e yazar ve yalnızca `product_id` içeren kalıcı RabbitMQ ingestion job'ı bırakır. Worker job'ı aldığında ürünün adını ve PDF konumunu PostgreSQL'den okur; ardından PDF'i Markdown'a çevirir, `data/processed` altına yazar ve Qdrant/BM25 indexlerini günceller. API `202 Accepted` ve `ingestion_status=queued` döndürür.

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Frontend: <http://localhost:3000>

Frontend şu an ürün listesini veritabanından çekmiyor. `frontend/src/data/product.ts` içindeki `product.id`, lokal test sırasında PostgreSQL'e upload edilen SecureHome ürününün gerçek UUID'siyle simüle edilmiştir. Yeni ürün oluşturulduğunda bu değer, upload response'undaki `product.id` ile değiştirilmelidir; kalıcı çözümde frontend upload response'unu state/store içinde tutup chat isteğine buradan gönderecektir.

Chat endpoint'i:

```http
POST /api/v1/chat
```

```json
{
  "question": "42 mm kapı için hangi montaj vidası kullanılmalı?",
  "product_id": "UPLOAD_RESPONSE_PRODUCT_ID"
}
```

## Ürün ve yorum endpoint'leri

Ürün için yalnızca RAG dokümanıyla eşleşen kimlik, ürün adı ve PDF konumu tutulur. Yorumlar ayrı endpoint üzerinden eklenir:

```http
POST /api/v1/products
POST /api/v1/products/{product_id}/reviews
GET /api/v1/products/{product_id}/reviews
GET /api/v1/products/{product_id}
GET /api/v1/products?skip=0&limit=20
PATCH /api/v1/products/{product_id}
DELETE /api/v1/products/{product_id}
```

Upload response'undaki `product.id` değerini chat isteğindeki `product_id` olarak kullanın. Frontend ürün ekranı statik kalabilir; önemli olan chat gönderilirken doğru ürün ID'sinin taşınmasıdır.

## Retrieval testi

```powershell
.venv\Scripts\python.exe -m scripts.search_product_retriever "42 mm kapı için hangi montaj vidası kullanılmalı?"
```

Hybrid retrieval testi:

```powershell
.venv\Scripts\python.exe -m scripts.search_hybrid_chunks "uygulama bağlantısı neden kopuyor"
```

## Gelecek aşamalar

| Aşama | Amaç |
|---|---|
| Review indexing | İşlenmiş yorumları Qdrant'a eklemek |
| Ingestion status | Ürün işleme durumunu PostgreSQL'de takip etmek |
| Tool calling | Stok, sipariş ve ürün verilerini kontrollü araçlarla sorgulamak |
| Evaluation set | Retrieval doğruluğunu ve regresyonları ölçmek |

## Proje durumu

Ürün upload, PostgreSQL kaydı, RabbitMQ job tüketimi, PDF ingestion, semantic search, BM25, hybrid retrieval, context expansion, reranking ve Mistral generation akışları çalışır durumdadır. Proje şu anda gerçek ürün PDF'leriyle kaynaklı cevap üretimini test eden prototip aşamasındadır.
