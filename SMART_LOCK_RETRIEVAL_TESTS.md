# SecureHome SHL-500 Retrieval Test Raporu

Tarih: 2026-09-25

## Test kapsamı

Yeni `SecureHome SHL-500 Smart Lock` PDF'i Docling ile Markdown'a çevrildi, temizlendi, başlıklara göre chunk'landı ve Qdrant + BM25 hybrid retrieval akışına alındı.

- İşlenen belge: 1 PDF
- Üretilen chunk: 68
- Kalite filtresine takılan chunk: 0
- Kullanılan arama: Semantic + BM25, RRF ile birleştirme
- Sonuç sayısı: `top_k=3`
- Aday havuzu: `candidate_k=15`

## Sonuçlar

### 1. 42 mm kapı kalınlığı ve vida seçimi

Soru:

> 42 mm kapı kalınlığı için hangi montaj vidasını kullanmalıyım?

Sonuç:

- Birinci sonuç 38 mm için mavi vida bilgisini getirdi.
- İkinci sonuç genel vida uyumluluk tablosunu getirdi.
- Üçüncü sonuç 40–50 mm aralığı için siyah vida bilgisini getirdi.

Değerlendirme: **Kısmi başarı.** 42 mm için doğru bilgi sonuçlarda mevcut: siyah vida. Ancak tablo chunk'ı ile açıklama chunk'ı ayrıldığı için cevap tek ve doğrudan bir chunk içinde gelmedi. Bu, tablo satırlarının aynı bölümde birleştirilmesi gerektiğini gösteriyor.

### 2. 38 mm delik çapı

Soru:

> Kapının mevcut delik çapı 38 mm ise ne yapmalıyım?

Birinci sonuç doğrudan şu bilgiyi verdi:

> 38 mm çapa sahip kapılar için kutu içerisindeki adaptör halkası kullanılmalıdır.

Değerlendirme: **Başarılı.** Doğru bölüm birinci sırada geldi; ayrıca standart 54 mm delik çapı ve 54 mm'den büyük deliklerin uyumsuzluğu da bulundu.

### 3. 70 mm backset

Soru:

> Backset mesafesi 70 mm ise kilit dili destekliyor mu?

Birinci sonuç doğrudan 60/70 mm ayar bölümünü getirdi:

> 70 mm ölçü için kilit dili saat yönünde çevrilerek uzatılmalıdır.

Değerlendirme: **Başarılı.** Hem ayar prosedürü hem de 60/70 mm destek bilgisi ilk sırada bulundu.

### 4. Pil tamamen bittiğinde acil açma

Soru:

> Piller tamamen biterse kilidi nasıl açabilirim?

Birinci sonuç iki acil yöntemi getirdi:

1. Dış gövdenin altındaki USB-C portuna 5V/1A powerbank bağlamak.
2. Gizli mekanik kapağı açıp fiziksel acil durum anahtarını kullanmak.

Değerlendirme: **Başarılı.** Doğru soru-cevap bölümü birinci sırada geldi.

### 5. DoorSense mıknatısı

Soru:

> DoorSense mıknatısı nasıl monte edilir?

Sonuçlar genel arıza, karşılık plakası ve backset bölümlerini getirdi. SecureHome SHL-500 dokümanında `DoorSense` adlı bir özellik bulunmuyor.

Değerlendirme: **Beklenen cevap üretilemedi.** Bu, retrieval'ın yanlış çalıştığı anlamına gelmez; soru başka bir ürünün özelliğine ait. Ancak generation katmanında veya ürün filtresi katmanında sistemin şu tür bir cevap verebilmesi gerekir:

> SecureHome SHL-500 dokümanlarında DoorSense desteği veya mıknatıs montajı bilgisi bulunamadı.

## Genel değerlendirme

İlk dört testte temel retrieval akışı kullanılabilir durumda. En önemli mevcut problem, teknik tabloların birden fazla chunk'a bölünmesi. Özellikle 42 mm vida sorusunda doğru bilgiler bulundu fakat tek bir bağlamda birleşmedi.

Sonraki iyileştirme adayları:

1. Teknik tablo satırlarını mümkün olduğunca tek chunk içinde tutmak.
2. Tablo başlığını her tablo parçasına eklemek.
3. Ürün dokümanında bulunmayan özellikler için düşük güven / cevap yok davranışı eklemek.
4. Generation katmanına geçildiğinde cevapta yalnızca retrieval'ın desteklediği bilgileri kullanmak.

## Context expansion düzeltmesi

42 mm testi sonrasında retrieval öncesi bağlam genişletme eklendi.

### Önce

```text
Semantic + BM25 adayları
→ Reranker
→ top_k sonuç
```

Bu akışta 42 mm sorusu için 38 mm FAQ'sı, genel tablo başlığı ve siyah vida bilgisi ayrı adaylar olarak geliyordu.

### Sonra

```text
Semantic + BM25 adayları
→ Aynı h2 altındaki parçaları bul
→ Aynı belgedeki komşu chunk'ları ekle
→ Reranker
→ top_k sonuç
```

Yeni kodun ana noktaları:

- `text_splitter.py` her chunk'a `chunk_index` ekler.
- `context_expander.py` aynı ürün, PDF ve bölüm içindeki ilişkili chunk'ları bulur.
- Aynı PDF'deki yakın chunk'lar da aday havuzuna eklenir.
- `product_retriever.py` bu genişletilmiş aday havuzunu reranker'a gönderir.

### After sonucu

42 mm sorusunun ProductRetriever çıktısında doğrudan şu bölüm 2. sırada bulundu:

```text
35-40 mm kapı için: Mavi vidalar
40-50 mm kapı için: Siyah vidalar
50-55 mm kapı için: Gümüş vidalar
```

Bu nedenle LLM artık yalnızca tek bir vida chunk'ı değil, tüm renk-kalınlık eşleştirmesini birlikte görebilecek.
