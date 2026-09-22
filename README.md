# Amazon Product Info User Chatbot

Bu proje, e-ticaret ürün dokümanlarını anlayıp kullanıcı sorularına kaynak dokümanlara dayalı cevaplar vermeyi amaçlayan bir RAG tabanlı ürün bilgi chatbot'udur.

Ürün bilgileri farklı PDF kataloglarından ve kullanım kılavuzlarından gelebilir. Bu nedenle ilk aşamada PDF'ler Docling ile Markdown'a dönüştürülür, temizlenir, ürün metadata'sı frontmatter olarak eklenir ve LangChain ile anlamlı parçalara ayrılır. Oluşturulan chunk'lar yerel embedding modeliyle vektörleştirilerek Qdrant'a kaydedilir.

## Mevcut pipeline

```text
PDF
  ↓
Docling Markdown
  ↓
Markdown temizleme + frontmatter metadata
  ↓
LangChain Markdown loader
  ↓
Başlık bazlı chunking
  ↓
multilingual-e5-small embedding
  ↓
Qdrant vector database
```

Şu an iki iPhone 14 dokümanı işlenmiş ve 109 chunk Qdrant'a yazılmıştır. Retrieval ve Mistral tabanlı cevap üretimi bir sonraki geliştirme aşamasıdır.

## Mimari

```text
src/
├── api/              # FastAPI endpoint'leri
├── core/             # Ayarlar ve uygulama altyapısı
├── rag/
│   ├── loaders/      # Docling ve Markdown yükleyicileri
│   ├── normalizers/  # Markdown temizleme ve frontmatter
│   ├── vectorstores/ # Embedding ve Qdrant bağlantısı
│   └── prompts/      # RAG prompt'ları
├── services/         # Ingestion ve chat iş mantığı
└── schemas/          # API veri modelleri
```

## Kurulum

Sanal ortamı oluşturup bağımlılıkları kurun:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Qdrant'ı Docker ile başlatın:

```powershell
docker compose up -d qdrant
```

## PDF'i Markdown'a dönüştürme

```powershell
.venv\Scripts\python.exe scripts\convert_pdf_to_markdown.py `
  "input.pdf" `
  "data\processed\product.md" `
  --product-id "PRODUCT-001" `
  --product-name "Product Name" `
  --source-type "technical_specs" `
  --raw-output "data\raw\product-raw.md"
```

## Chunk'ları kontrol etme

```powershell
.venv\Scripts\python.exe -m scripts.inspect_chunks
```

## Qdrant'a ingestion

```powershell
.venv\Scripts\python.exe -m scripts.ingest
```

Qdrant dashboard: <http://localhost:6333/dashboard>

## Yol haritası

- Retrieval kalitesini soru-cevap testleriyle ölçmek.
- Mistral ile context tabanlı cevap üretimini tamamlamak.
- Duplicate doküman ve chunk kontrolü eklemek.
- `document_id`, dosya hash'i ve versiyonlama eklemek.
- Büyük PDF işlemlerini background worker'a taşımak.
- Parser, tablo ve ingestion kalite kontrollerini artırmak.
- Gerekirse chunk'lar için sentetik kullanıcı soruları üretip reverse index oluşturmak.
