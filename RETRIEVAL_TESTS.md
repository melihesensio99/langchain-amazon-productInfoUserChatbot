# Retrieval Testleri

Bu dosya, Qdrant retrieval katmanının manuel test sonuçlarını ve kalite değerlendirmelerini tutar.

## Test 1 - iPhone 14 ekran boyutu

### Sorgu

```text
iPhone 14 ekran boyutu nedir
```

### Komut

```powershell
.venv\Scripts\python.exe -m scripts.search_chunks `
  "iPhone 14 ekran boyutu nedir" `
  --top-k 3 `
  --product-id IPHONE-14
```

### Sonuç 1

```text
score: 0.9119
product_id: IPHONE-14
source_type: technical_specs
h2: iPhone 14 - Teknik Özellikler
```

İçerik, sorunun cevabını doğrudan içeriyor:

```text
Standart bir dikdörtgen olarak ölçüldüğünde ekran diyagonal olarak 6.06 inçtir.
```

Değerlendirme: **Doğru ve yeterli.**

### Sonuç 2

```text
score: 0.8733
product_id: IPHONE-14
source_type: technical_specs
```

İçerik:

```text
Boyut ve ağırlık, yapılandırmaya ve üretim sürecine göre değişir.
```

Değerlendirme: **Kısmen ilişkili, ancak sorunun doğrudan cevabını içermiyor.**

### Sonuç 3

```text
score: 0.8696
product_id: IPHONE-14
source_type: technical_specs
```

İçerik Apple destek sayfasının footer/boilerplate bölümünden geliyor:

```text
Yararlı buldunuz mu?
Destek iPhone 14 - Teknik Özellikler Kullanım Şartları
Site Haritası
```

Değerlendirme: **Alakasız gürültü.**

## Genel değerlendirme

Doğru cevap ilk sırada bulunuyor. Ancak ikinci ve üçüncü sonuçlarda gereksiz içerik var. Bu nedenle mevcut retrieval durumu:

```text
Doğru chunk bulunuyor: Evet
Top-1 kalitesi: İyi
Top-3 gürültüsü: Var
```

## Sonraki iyileştirmeler

- [ ] Footer, site haritası ve kullanım şartları gibi boilerplate içerikleri temizle.
- [ ] Çok kısa veya yalnızca navigasyon içeren chunk'ları filtrele.
- [ ] Bölüm başlıklarının parser tarafından doğru aktarılmasını kontrol et.
- [ ] `score_threshold` değerini test et.
- [ ] Gerekirse reranker veya hibrit arama ekle.

## Test 1 - Boilerplate filtresi sonrası

Kalite filtresi `split_markdown_documents()` içine bağlandı. Qdrant collection temizlenip yeniden ingestion yapıldı.

```text
Önce: 109 chunk
Sonra: 94 chunk
Çıkarılan: 15 heading-only chunk ve 1 boilerplate chunk
```

Tekrar yapılan aynı sorguda footer sonucu artık dönmedi. Yeni üçüncü sonuç, footer yerine ürünün renk seçenekleri gibi gerçek ürün içeriği oldu. Teknik değer taşıyan tek satırlı başlıklar, örneğin `Genişlik: 71,5 mm ... Ağırlık: 172 gram`, korunmuştur.
