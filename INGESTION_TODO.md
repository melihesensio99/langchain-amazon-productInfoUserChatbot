# Ingestion Katmanı - Production İyileştirmeleri

Temel ingestion akışı tamamlandı:

```text
PDF → Docling → Markdown → frontmatter → loader → chunking → embedding → Qdrant
```

## Yapılacak iyileştirmeler

- [x] Aynı doküman tekrar işlendiğinde duplicate chunk oluşmasını engelle.
- [x] Her chunk için deterministik ID üret.
- [x] Qdrant'a yazmadan önce mevcut ID'lerle eski chunk'ları temizle veya güncelle.
- [x] Chunk sınırları PDF güncellemesiyle kaydığında stale chunk'ları temizleyip güvenli full sync yap.
- [x] BM25 index'ini ingestion sırasında oluşturup `data/indexes/` altında kaydet.
- [ ] Boş, çok kısa ve anlamsız başlık-only chunk'larını filtrele.
- [ ] Büyük PDF işlemlerini API request'inden ayırıp background job/worker kullan.
- [ ] Ingestion başlangıç, başarı ve hata loglarını ekle.
- [ ] Parser çıktısı ve tablo bütünlüğü için kalite kontrolleri ekle.
- [x] Docling'in teknik özellik satırlarını yanlışlıkla `h2` başlığına dönüştürmesini düzelt.
- [x] Düzeltme sonrası iPhone 14 retrieval sonucunu tekrar kontrol et; `h2` artık `"Boyut ve Ağırlık"`, alanlar `page_content` içinde ayrı satırlar olarak geliyor.
- [x] İçindekiler/TOC bloklarını ingestion öncesi temizle ve nokta çizgili navigation chunk'larını kalite filtresinde ele.
- [ ] Ürün, doküman tipi ve versiyon metadata filtrelerini destekle.
- [ ] Başarısız dosyaları ve tekrar denenebilir ingestion durumlarını kaydet.
- [ ] Chunk sayısı, işlenen dosya ve hata özetini API response'unda raporla.

## Düzeltilen hata: teknik özelliklerin yanlışlıkla başlık olması

### Problem

Docling bazı kataloglarda birden fazla teknik alanı tek bir Markdown başlığına
birleştirebiliyordu:

```markdown
## Genişlik: 71,5 mm Uzunluk: 146,7 mm Derinlik: 7,80 mm Ağırlık: 172 gram
```

Bu durumda `MarkdownHeaderTextSplitter`, teknik değerlerin tamamını `h2`
metadata'sı olarak algılıyordu. Sonuç olarak bölüm başlığı yanlış görünüyordu ve
retrieval çıktısı şu hale geliyordu:

```python
{"h2": "Genişlik: 71,5 mm ... Ağırlık: 172 gram"}
```

### Çözüm

`src/rag/normalizers/markdown_cleaner.py` içindeki
`_normalize_technical_heading()` fonksiyonu, kategoriye özel alan isimlerini
hardcode etmeden genel `alan: değer` desenini algılıyor. Bir `##` satırında en
az iki yapılandırılmış alan bulunursa satır başlık olarak bırakılmıyor; alanlar
Markdown listesine dönüştürülüyor:

```markdown
## Boyut ve Ağırlık

- Genişlik: 71,5 mm
- Uzunluk: 146,7 mm
- Derinlik: 7,80 mm
- Ağırlık: 172 gram
```

Bu kural yalnızca telefonlara özel değildir. Örneğin aşağıdaki katalog satırı da
aynı şekilde işlenebilir:

```markdown
## Renk: Siyah Beden: 42 Malzeme: Deri
```

Sonuç:

```markdown
## Özellikler

- Renk: Siyah
- Beden: 42
- Malzeme: Deri
```

### Doğrulama

Formatter değişikliğinden sonra ingestion tekrar çalıştırıldı ve Qdrant ile
BM25 index güncellendi. Toplam `94` chunk yeniden indekslendi. Retrieval testi:

```powershell
.\.venv\Scripts\python.exe -m scripts.search_product_retriever "iPhone 14 kaç gram"
```

Beklenen ve gözlenen metadata:

```python
{"h2": "Boyut ve Ağırlık"}
```

`Ağırlık: 172 gram` bilgisi artık `h2` içinde değil, chunk'ın
`page_content` alanında bulunuyor.

## Gelecek retrieval iyileştirmesi: sentetik soru üretimi

- [ ] Her anlamlı chunk için hafif bir modelle, chunk'ın cevaplayabileceği doğal kullanıcı sorularını üret.
- [ ] Üretilen soruları `parent_chunk_id` ile orijinal chunk'a bağla.
- [ ] Sentetik soruları orijinal chunk'la birlikte veya ayrı bir reverse index'te embed et.
- [ ] Üretim öncesi soruların chunk içeriğiyle gerçekten desteklendiğini doğrula.
- [ ] Semantic ve hybrid retrieval ile karşılaştırmalı Recall@K testi yap.

## Retrieval baseline testi - 10 ürün

TOC temizleyicisi eklendikten sonra 10 PDF yeniden işlendi. Chunk sayısı
`1217`'den `1188`'e düştü; fark çoğunlukla içindekiler ve navigation
parçalarından oluşuyor. Qdrant koleksiyonu da yeni `1188` chunk ile güncellendi.

### Sonuç özeti

| Soru tipi | Sonuç |
|---|---|
| Z Fold 8 kamera çözünürlüğü | Doğru ürün ve teknik belge ilk sırada |
| Z Fold 8 ekran görüntüsü | Doğru ürün ve kullanım kılavuzu ilk sırada |
| MSI monitör ayağı | Doğru bölüm ilk sırada |
| TV panel kilidi | Doğru bölüm ilk sırada |
| iPhone 16 depolama | Ürün doğru, fakat kapasite bölümü ilk sırada değil |
| AirPods Max 2 ses teknolojisi | Ürün doğru; product_id filtresiyle doğru bölüm ilk sırada |

Bu test, metadata filtresinin ürün sayfası bağlamında faydalı olduğunu ve bazı
sorularda doğru ürünü bulmanın tek başına yeterli olmadığını gösteriyor. iPhone
16 kapasite örneği için sonraki aday iyileştirmeler reranker, query expansion
veya teknik değerleri (ör. `128 GB`) güçlendiren keyword ağırlığıdır.

Bu yöntem, kullanıcıların günlük konuşma diliyle sorduğu soruların teknik doküman chunk'larıyla eşleşmesini iyileştirebilir. Şimdilik uygulanmayacak; önce mevcut semantic retrieval ve keyword/hybrid retrieval baseline'ları ölçülecek.

## Mevcut durum

- 10 Markdown dokümanı işleniyor.
- Son temizleme ve tablo-korumalı chunking sonrasında `1287` chunk Qdrant'a yazıldı.
- Qdrant koleksiyonu: `amazon_products`.

## Son chunk düzeltmeleri (2026-09-24)

- Markdown tabloları satır ortasında bölünmüyor; tablo başlığı ve satırları
  birlikte korunuyor. Uzun tablolar yalnızca satır sınırlarından bölünüyor.
- Docling'in teknik değerleri yanlışlıkla `h2` yaptığı genel `alan: değer`
  başlıkları normal metin/listelere dönüştürülüyor. Bu kural kategoriye özel
  değil; telefon, bilgisayar, ayakkabı veya başka kataloglara uygulanabilir.
- Dekoratif başlık çizgileri (`\\_\\_\\_...`) metadata ve içerikten temizleniyor.
- `İÇİNDEKİLER` başlığı açıkça görünmese bile noktalı lider + sayfa numarası
  veya içindekiler başlıklı Markdown tablo deseniyle navigation blokları
  chunk'lanmadan eleniyor.
- Aynı ürün ve kaynak içindeki birebir tekrar chunk'lar tekilleştiriliyor.
- Markdown loader da dosyayı okurken temizleyiciyi çalıştırıyor; eski işlenmiş
  Markdown dosyaları yeniden oluşturulmadan da aynı kurallar uygulanıyor.
- İşlenmiş Markdown dosyaları manifest üzerinden yeniden yazıldı. Kontrol
  karakterleri, `�/ï¿½` replacement karakterleri ve yaygın `€/›` Türkçe
  karakter kalıntıları temizlendi.

Bu değişikliklerden sonra Qdrant ve diskteki BM25 index yeniden oluşturuldu.
Chunk kalitesi iyileşti; ancak `RAM` veya `depolama` gibi katalogdaki alan
adından farklı kullanıcı ifadelerinde doğru teknik tabloyu ilk sıraya taşıma
problemi retrieval/reranking katmanına aittir, chunk temizleme problemi değildir.

Teknik sayfalarda link olarak gelen bölüm etiketi ile yanlış `##` başlığın
eşleştiği durumlar için de genel bir düzeltme eklendi. Linkin hemen ardından
teknik alan/değer çiftleri geliyorsa link bölüm başlığı olarak korunuyor;
yanlış başlık kaldırılıyor. Örneğin Samsung çıktısındaki `Kamera` metadata'sı
`Ekran` olarak düzeltildi ve index yeniden oluşturuldu. Son testte doğru `Ekran`
chunk'ı bulundu; ancak retrieval sıralaması hâlâ reranker/source-type önceliği
gerektiriyor.

## Reranker

`src/rag/rerankers/cross_encoder.py` ile semantic + BM25 adaylarının üzerine
çok dilli `BAAI/bge-reranker-v2-m3` CrossEncoder eklendi. Model lazy-load edilir;
yalnızca ilk retrieval isteğinde yüklenir. Aday havuzu `30` chunk'a çıkarılır,
reranker ise son `top_k` sonucu seçer. İlk testlerde reranker aktif çalıştı;
ancak `ana ekran kaç inç?` gibi teknik belge türü belirsiz sorularda kullanım
kılavuzunu tamamen geride bırakamadı. Bu nedenle sonraki retrieval adımı,
reranker skoruna `source_type` intent önceliği eklemektir.

20 adaylık A/B testi yapıldı. Reranker gecikmesi yaklaşık 10–19 saniyeye
geriledi; ancak iPhone 16 kapasite chunk'ı ilk aşamadaki 26. sırada kaldığı için
20 aday arasına giremedi ve sonuç kayboldu. Bu nedenle mevcut RRF çıktısını
20'de kesmek yerine 30 adaylık güvenli ayar korundu. Daha düşük aday sayısı için
semantic ve BM25 listelerini ayrı alıp dengeli bir birleşim yapmak gerekiyor.

Bu aday havuzu yapısı uygulandı: semantic ve BM25 ayrı ayrı `15` aday üretir,
duplicate'ler temizlenir ve en fazla `30` aday reranker'a gider. Böylece RRF'nin
tek bir ortak sıralamasında geriye düşen BM25 sonuçları korunur. Aynı testte
reranker sonrası `Recall@1=0.83`, `Recall@3=1.00`, `Recall@5=1.00`, `MRR=0.89`
ölçüldü; iPhone 16 kapasite chunk'ı artık aday havuzuna girip 3. sıraya çıktı.

Semantic/BM25 ağırlıkları `0.5 / 0.5` olarak da test edildi. Baseline'da
Samsung ana ekran sorusu 2. sıradan 3. sıraya geriledi; iPhone kapasite sorusu
26. sırada kaldı. Reranker sonrası metrikler değişmedi:
`Recall@1=0.83`, `Recall@3=1.00`, `Recall@5=1.00`, `MRR=0.92`. Bu test setinde
eşit ağırlık, reranker'ın üstüne ek bir kalite artışı sağlamadı; ayar şu an
`product_retriever.py` içinde `0.5 / 0.5` olarak bırakıldı.

PDF'deki kelime kutularının yanlış ayrıştırılmasından kaynaklanan `S mart
Switc h` veya `dokun un` gibi kelime-içi boşluklar ise encoding hatası değildir.
Temizleyici, birleşik kelimenin aynı belgede doğru biçimde başka bir yerde
geçtiğini kanıt olarak kullanarak `S mart` → `Smart`, `Switc h` → `Switch` ve
benzerlerini genel biçimde birleştiriyor. Belgenin hiçbir yerinde doğru biçimi
geçmeyen `dokun un` gibi örnekler ise sözlük/LLM desteği olmadan güvenli biçimde
geri kazanılamaz; bunları kategoriye özel kelime listesiyle zorla birleştirmek
başka ürünlerde yanlış düzeltmelere yol açabilir.
