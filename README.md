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

## PDF'leri Markdown'a dönüştürme

Birden fazla hazır PDF için `data/document_manifest.yaml` kullanılır.
Manifest, aynı ürüne ait teknik özellik ve kullanım kılavuzu gibi ayrı PDF'leri
aynı `product_id` altında toplar; `brand` ve `source_type` gibi alanları da
frontmatter metadata'sına taşır.

```powershell
Copy-Item data\document_manifest.example.yaml data\document_manifest.yaml
# source_dir ve documents alanlarını kendi PDF'lerinize göre düzenleyin.
.venv\Scripts\python.exe -m scripts.convert_manifest data\document_manifest.yaml
```

Ham Markdown zaten oluşturulduysa Docling'i tekrar çalıştırmadan yalnızca
manifest metadata'sını uygulayabilirsiniz:

```powershell
.venv\Scripts\python.exe -m scripts.apply_manifest_metadata data\document_manifest.yaml
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

## Ürün sayfası chatbot isteği

Frontend seçili ürünün ID'sini gönderirse semantic ve BM25 retrieval aynı ürünle
sınırlandırılır:

```json
POST /api/v1/chat
{
  "question": "Kaç gram?",
  "product_id": "APPLE-IPHONE-14"
}
```

`product_id` gönderilmezse genel katalog araması yapılır.

## Yol haritası

- Retrieval kalitesini soru-cevap testleriyle ölçmek.
- Mistral ile context tabanlı cevap üretimini tamamlamak.
- Duplicate doküman ve chunk kontrolü eklemek.
- `document_id`, dosya hash'i ve versiyonlama eklemek.
- Büyük PDF işlemlerini background worker'a taşımak.
- Parser, tablo ve ingestion kalite kontrollerini artırmak.
- Gerekirse chunk'lar için sentetik kullanıcı soruları üretip reverse index oluşturmak.
