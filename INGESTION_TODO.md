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
- [ ] Ürün, doküman tipi ve versiyon metadata filtrelerini destekle.
- [ ] Başarısız dosyaları ve tekrar denenebilir ingestion durumlarını kaydet.
- [ ] Chunk sayısı, işlenen dosya ve hata özetini API response'unda raporla.

## Mevcut durum

- 2 Markdown dokümanı işleniyor.
- 109 chunk Qdrant'a yazıldı.
- Qdrant koleksiyonu: `amazon_products`.
