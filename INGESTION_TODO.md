# Ingestion Katmanı - Production İyileştirmeleri

Temel ingestion akışı tamamlandı:

```text
PDF → Docling → Markdown → frontmatter → loader → chunking → embedding → Qdrant
```

## Yapılacak iyileştirmeler

- [ ] Aynı doküman tekrar işlendiğinde duplicate chunk oluşmasını engelle.
- [ ] Her doküman için sabit `document_id` ve mümkünse dosya hash'i üret.
- [ ] Qdrant'a yazmadan önce mevcut `document_id` ile eski chunk'ları temizle veya güncelle.
- [ ] Boş, çok kısa ve anlamsız başlık-only chunk'larını filtrele.
- [ ] Büyük PDF işlemlerini API request'inden ayırıp background job/worker kullan.
- [ ] Ingestion başlangıç, başarı ve hata loglarını ekle.
- [ ] Parser çıktısı ve tablo bütünlüğü için kalite kontrolleri ekle.
- [ ] Docling'in genişlik, uzunluk ve ağırlık gibi teknik özellik satırlarını yanlışlıkla `h2` başlığına dönüştürmesini düzelt; mevcut hata örneği `h2: "Genişlik: 71,5 mm ... Ağırlık: 172 gram"`.
- [ ] Düzeltme sonrası aynı iPhone 14 chunk'ını tekrar kontrol et; beklenen yapı `h2: "Boyut ve Ağırlık"` ve ağırlık bilgisinin `page_content` içinde ayrı bir özellik satırı olmasıdır.
- [ ] Ürün, doküman tipi ve versiyon metadata filtrelerini destekle.
- [ ] Başarısız dosyaları ve tekrar denenebilir ingestion durumlarını kaydet.
- [ ] Chunk sayısı, işlenen dosya ve hata özetini API response'unda raporla.

## Gelecek retrieval iyileştirmesi: sentetik soru üretimi

- [ ] Her anlamlı chunk için hafif bir modelle, chunk'ın cevaplayabileceği doğal kullanıcı sorularını üret.
- [ ] Üretilen soruları `parent_chunk_id` ile orijinal chunk'a bağla.
- [ ] Sentetik soruları orijinal chunk'la birlikte veya ayrı bir reverse index'te embed et.
- [ ] Üretim öncesi soruların chunk içeriğiyle gerçekten desteklendiğini doğrula.
- [ ] Semantic ve hybrid retrieval ile karşılaştırmalı Recall@K testi yap.

Bu yöntem, kullanıcıların günlük konuşma diliyle sorduğu soruların teknik doküman chunk'larıyla eşleşmesini iyileştirebilir. Şimdilik uygulanmayacak; önce mevcut semantic retrieval ve keyword/hybrid retrieval baseline'ları ölçülecek.

## Mevcut durum

- 2 Markdown dokümanı işleniyor.
- 109 chunk Qdrant'a yazıldı.
- Qdrant koleksiyonu: `amazon_products`.
