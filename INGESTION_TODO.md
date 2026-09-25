# Ingestion Katmanı

Bu dosya mevcut test verisine ve güncel ingestion pipeline'ına göre tutulur.

## Mevcut test verisi

Şu an ingestion'a dahil edilen ürün:

```text
SecureHome SHL-500 Smart Lock
product_id: SECUREHOME-SHL-500
source_type: technical_and_manual
```

İşlenmiş kaynak:

```text
data/processed/securehome-shl-500-technical-and-manual.md
```

Güncel temel akış:

```text
PDF
  ↓
Docling ham Markdown
  ↓
Markdown cleaner + formatter
  ↓
Frontmatter metadata
  ↓
Markdown loader
  ↓
Markdown/table-aware chunking
  ↓
Chunk quality filter
  ↓
Embedding
  ↓
Qdrant + BM25 index
```

## Tamamlanan ingestion özellikleri

- [x] Manifest üzerinden ürün, dosya ve `source_type` eşleştirme.
- [x] Docling PDF çıktısını işlenmiş Markdown'a dönüştürme.
- [x] Frontmatter metadata'sını LangChain `Document.metadata` içine aktarma.
- [x] Markdown başlıklarını ve bölüm hiyerarşisini chunk metadata'sına taşıma.
- [x] Chunk başına ürün ve bölüm breadcrumb context'i ekleme.
- [x] Tablo başlığı ve satırlarını mümkün olduğunca birlikte koruma.
- [x] Uzun tabloları satır sınırlarından bölme.
- [x] Boş, başlık-only, footer ve düşük bilgi yoğunluklu chunk'ları eleme.
- [x] Kontrol karakterlerini, image placeholder'larını ve dekoratif parser artıklarını temizleme.
- [x] İçindekiler ve navigation bloklarını chunk'lamadan önce eleme.
- [x] Aynı kaynak içindeki birebir tekrar chunk'ları tekilleştirme.
- [x] Teknik alan/değer satırlarının yanlışlıkla `h2` olarak yazılmasını genel kuralla düzeltme.
- [x] Deterministic chunk ID üretme.
- [x] Qdrant'ta eski/stale chunk'ları full sync ile temizleme veya güncelleme.
- [x] BM25 index'ini ingestion sonrasında güncelleme.
- [x] Güncel SecureHome verisini Qdrant'a yeniden indexleme.

## Genel parser temizliği

Cleaner ürün kategorisini tahmin etmeye veya içeriği elle yeniden yazmaya çalışmaz. Farklı ürün türlerinde güvenli olan yapısal temizlikleri uygular:

- Bozuk kontrol karakterlerini ve replacement karakterlerini kaldırır.
- Gereksiz footer, navigation ve tekrar eden link bloklarını azaltır.
- Markdown başlıklarındaki dekoratif çizgileri temizler.
- HTML entity ve gereksiz boşlukları normalize eder.
- Tablo ayraçlarını ve satır yapısını korumaya çalışır.
- Teknik alan/değer çiftlerini tek bir yanlış başlık olmaktan çıkarır.

Örnek problem:

```markdown
## Genişlik: 71,5 mm Uzunluk: 146,7 mm Ağırlık: 172 gram
```

Genel normalizasyon sonrası bilgi başlık metadata'sına değil, içerik alanına taşınır:

```markdown
## Boyut ve Ağırlık

- Genişlik: 71,5 mm
- Uzunluk: 146,7 mm
- Ağırlık: 172 gram
```

Bu kural telefonlara özel değildir; laptop, smart lock, televizyon veya farklı kataloglardaki benzer `alan: değer` yapılarını hedefler.

## Mevcut kalite notları

### OCR kelime bölünmeleri

Görsel ağırlıklı PDF'lerde OCR bazen `dokun un`, `başlat ın` veya `S mart` gibi kelime-içi boşluklar üretebilir. Güvenli normalizer yalnızca belgenin başka bir yerinde doğru yazım için yeterli kanıt varsa otomatik birleştirme yapar. Aksi halde kategoriye özel kelime listesiyle zorla düzeltme yapmak başka ürünlerde yanlış sonuç üretebilir.

### Tablo bölünmeleri

Docling bazı PDF tablolarını sayfa veya görsel sınırında bölebilir. Mevcut splitter tablo satırlarını korur ve ilgili bölüm context'ini ekler; ancak kötü OCR ile tamamen kaybolan bir hücreyi ingestion sonradan güvenilir biçimde tahmin edemez.

### Metadata sınırı

`product_id`, ürün adı ve belge türü manifest veya ileride admin panelinden gelir. Kullanıcının sorusundan ürün ID'si tahmin etmek zorunda değiliz; ürün sayfası seçili ürünün ID'sini endpoint'e gönderir. Retrieval bu ID ile Qdrant payload filtresi uygular.

## Sıradaki ingestion işleri

- [ ] PDF kalite raporu üret: sayfa, boş sayfa, OCR uyarısı ve tablo sayısını raporla.
- [ ] Her işlenmiş doküman için kaynak hash'i ve versiyon metadata'sı ekle.
- [ ] Başarısız PDF'leri ve tekrar denenebilir ingestion durumunu kaydet.
- [ ] Ingestion başlangıç, başarı ve hata loglarını yapılandır.
- [ ] Chunk sayısı, filtrelenen chunk sayısı ve hata özetini API response'unda raporla.
- [ ] Büyük PDF'leri API request'inden ayırıp background worker'a taşı.
- [ ] Teknik tablo bütünlüğü için otomatik inspection/evaluation testi ekle.
- [ ] Yeni ürünler eklendiğinde yalnızca değişen kaynakları yeniden embed et.

## Yorumların ileride ingestion'a eklenmesi

Kullanıcı yorumları teknik PDF'lerle aynı dosyadan gelmeyecek. Önce PostgreSQL'e yazılacak, sentiment worker tarafından işlenecek ve sonra ayrı bir kaynak türü olarak Qdrant'a aktarılacak:

```text
PostgreSQL review
  ↓
RabbitMQ review.created
  ↓
Sentiment worker
  ↓
Review Document + metadata
  ↓
Embedding ve Qdrant upsert
```

Örnek review metadata'sı:

```python
{
    "product_id": "SECUREHOME-SHL-500",
    "source_type": "product_review",
    "review_id": 42,
    "rating": 3,
    "sentiment": "mixed",
}
```

## Eski test verilerinin durumu

Önceki iPhone, Samsung, Grundig, MSI, TV ve diğer ürünlere ait ham/işlenmiş dosyalar mevcut test setinden çıkarıldı. Bu dosyalar güncel ingestion doğrulaması için kaynak kabul edilmez; yeni ürünler eklendiğinde aynı manifest → formatter → loader → chunk → index akışı kullanılacaktır.
