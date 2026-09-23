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

## Test 1 - Breadcrumb sonrası

Chunk içeriğinin başına belge ve bölüm bağlamı eklendi:

```text
[Belge: Apple iPhone 14 | Bölüm: Apple iPhone 14 > ...]
```

`iPhone 14'ün ağırlığı nedir` sorgusunda ağırlık chunk'ı artık ilk sırada geldi:

```text
score: 0.9394
```

## Before / After - Ağırlık sorgusu

### Sorgu

```text
iPhone 14'ün ağırlığı nedir
```

### Before - Breadcrumb olmadan

```text
Result 1: Genel iPhone 14 teknik özellikleri
Result 2: Boyut ve ağırlıkla ilgili genel açıklama
Result 3: Geri dönüştürülmüş malzemeler
```

Doğru teknik değer chunk'ı ilk üç sonuçta görünmüyordu. `Ağırlık: 172 gram` içeren chunk, doğal soruyla yeterince üst sıraya çıkamıyordu.

### After - Breadcrumb ile

Chunk'ın embedding'e giden metnine belge ve bölüm bağlamı eklendi:

```text
[Belge: Apple iPhone 14 | Bölüm: ... Ağırlık: 172 gram]
```

Sonuç:

```text
Result 1 | score=0.9394
Genişlik: 71,5 mm ... Ağırlık: 172 gram
```

Değerlendirme: Breadcrumb, teknik değer chunk'ının doğal kullanıcı sorusuyla eşleşmesini iyileştirdi ve doğru chunk'ı üçüncü sıradan birinci sıraya taşıdı.

## Test 2 - Semantic search'in kapasite sorgusunda yetersiz kalması

### Sorgu

```text
iPhone 14 hangi depolama seçeneklerine sahip
```

### Komut

```powershell
python -m scripts.search_chunks `
  "iPhone 14 hangi depolama seçeneklerine sahip" `
  --top-k 3 `
  --score-threshold 0.90
```

### Sonuç

```text
Sonuç bulunamadı.
```

Aynı sorgu daha düşük eşik ve daha geniş aday sayısıyla incelendiğinde doğru `Kapasite` chunk'ı bulundu, ancak üst sıralarda değildi:

```text
Kapasite chunk skoru: 0.8931
TrueDepth Kamera chunk skoru: 0.8912
```

`Kapasite` chunk'ının içeriği:

```text
128 GB
256 GB
512 GB
```

### Değerlendirme

Bu test üç problemi gösteriyor:

1. `score_threshold=0.90`, doğru chunk'ın `0.8931` skorunu eledi.
2. Threshold düşürüldüğünde bile `TrueDepth Kamera` gibi alakasız bir chunk daha üst sıraya çıktı.
3. Doğru kapasite chunk'ı mevcut olmasına rağmen doğal dildeki “depolama seçenekleri” ifadesiyle yeterince iyi eşleşmedi.

Sonuç olarak yalnızca `top_k` ve skor eşiğini ayarlamak yeterli değildir. `kapasite`, `depolama` ve `GB` gibi kritik kelimeleri doğrudan dikkate alan keyword search, semantic sonuçlarla birleştirilmelidir.

Bu test, hybrid search eklenmesi için retrieval katmanındaki somut kanıttır.

## Test 3 - BM25 keyword retrieval

BM25 prototipi `keyword_retriever.py` içinde oluşturuldu. Manuel test komutu:

```powershell
python -m scripts.search_keyword_chunks "iPhone 14 kapasite 128 GB" --top-k 3
```

### Teknik terimlerle başarılı sonuç

İlk sonuç doğru kapasite chunk'ı oldu:

```text
Keyword Result 1 | score=24.8655
h2: Kapasite
128 GB
256 GB
512 GB
```

Diğer sonuçların skorları daha düşüktü:

```text
Keyword Result 2 | score=7.9604
Keyword Result 3 | score=3.9377
```

Değerlendirme: **BM25, teknik terimler ve sayısal değerler doğrudan sorguda bulunduğunda doğru chunk'ı ilk sıraya taşıdı.**

### Doğal dil sorgusu

```powershell
python -m scripts.search_keyword_chunks "iPhone 14 hangi depolama seçeneklerine sahip" --top-k 3
```

Sonuçlarda ilk sıraya kapasite chunk'ı yerine şu içerik geldi:

```text
Apple'ın kararlılığı hakkında bilgi edinin
Depolama kapasitesi yazılım sürümüne, ayarlara ve iPhone modeline göre değişebilir.
```

Diğer sonuçlar da `Çip` ve `QuickType klavye desteği` bölümleriydi.

Değerlendirme: **BM25 doğal dildeki anlam ilişkilerini kendiliğinden kuramıyor.** `depolama` kelimesi footer içeriğinde geçtiği için bu chunk yukarı çıktı; `Kapasite` başlığı ise sorguda birebir geçmediği için doğru chunk bulunamadı.

### Keyword retrieval sonucu

```text
Teknik terim ve sayısal değer araması: Başarılı
Doğal dil ve eş anlamlı ifade araması: Sınırlı
Ana chatbot akışına doğrudan bağlama: Hazır EnsembleRetriever aşamasında yapıldı
Manuel BM25 prototipi: Test/debug amacıyla korunuyor

## Test 5 - LangChain hazır retriever bileşenleri

Ana chatbot akışında özel `HybridRetriever` yerine LangChain'in hazır bileşenleri kullanıldı:

```text
Qdrant semantic retriever
+
BM25Retriever
→ EnsembleRetriever
→ final top_k chunk
```

`product_retriever.py` artık bu hazır ensemble'ı döndürüyor. Test:

```text
iPhone 14 kapasite 128 GB
```

Sonuç: `Kapasite` chunk'ı ilk sırada geldi.

Doğal dil testi:

```text
iPhone 14 hangi depolama seçeneklerine sahip
```

Sonuçlarda semantic ve BM25 bileşenleri birleşse de `Kapasite` chunk'ı ilk sıraya çıkmadı. Bu, hazır `EnsembleRetriever` kullanımının doğru olduğunu; ancak doğal dil eş anlamlılık probleminin ayrıca çözülmesi gerektiğini gösterir. Query expansion şu an özellikle eklenmemiştir.

## Test 6 - Manuel hybrid ve hazır EnsembleRetriever karşılaştırması

Aynı sorgu iki farklı akışla çalıştırıldı:

```text
iPhone 14 kapasite 128 GB
```

### Manuel hybrid

```text
1. Kapasite
2. Apple'ın kararlılığı hakkında bilgi edinin
3. Genişlik / Ağırlık
4. TrueDepth Kamera
5. iPhone ve Çevre
```

Manuel akış ayrıca kendi RRF skorunu gösterdi:

```text
Kapasite rrf_score: 0.032787
```

### Ana product retriever

Ana akışta kullanılan hazır `BM25Retriever + EnsembleRetriever` aynı sorguda aynı sıra düzenini döndürdü:

```text
1. Kapasite
2. Apple'ın kararlılığı hakkında bilgi edinin
3. Genişlik / Ağırlık
4. TrueDepth Kamera
5. Çift kamera sistemi
```

Hazır ensemble sonuçları `Document` olarak döndürdüğü için ham RRF skorunu yazdırmadı.

Değerlendirme: **Bu testte manuel hybrid ve LangChain'in hazır ensemble akışı aynı doğru ilk sonucu verdi.** Manuel uygulama debug ve skor inceleme için korunuyor; ana chatbot akışında hazır LangChain bileşenleri kullanılıyor.

## Test 4 - Hybrid retrieval prototipi

Hybrid retriever, semantic ve BM25 sonuçlarını ham skorları toplamadan, sonuç sıralarını kullanan Reciprocal Rank Fusion (RRF) ile birleştirir.

Manuel test komutu:

```powershell
python -m scripts.search_hybrid_chunks "iPhone 14 kapasite 128 GB" --top-k 3 --candidate-k 10
```

Teknik terim içeren sorguda doğru sonuç ilk sıraya geldi:

```text
Hybrid Result 1
h2: Kapasite
128 GB
256 GB
512 GB
```

Doğal dil sorgusunda ise:

```text
iPhone 14 hangi depolama seçeneklerine sahip
```

`Kapasite` chunk'ı semantic sıralamada 66. sırada kaldı ve BM25 sorgusunda da `kapasite` kelimesi geçmediği için aday listesine giremedi. Bu nedenle hybrid sonuçlarda footer ve kamera chunk'ları üstte kaldı.

Değerlendirme: **Hybrid altyapısı çalışıyor ve teknik terimlerde iyileştirme sağlıyor; doğal dildeki eş anlamlı ifadeler için query expansion veya daha iyi sparse/keyword sorgu üretimi ileride ayrıca değerlendirilecek.** Query expansion şu an uygulanmıyor.
```
