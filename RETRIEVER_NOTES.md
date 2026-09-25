# Retriever Notları

Bu dosya mevcut SecureHome SHL-500 verisi ve gerçek product retriever akışını açıklar.

## 1. `get_vector_store()` ne yapar?

Dosya:

```text
src/rag/vectorstores/qdrant.py
```

`get_vector_store()` bizim yazdığımız factory fonksiyonudur. Qdrant client'ı, collection'ı ve embedding adapter'ını hazırlar; tek başına arama yapmaz.

```text
get_vector_store()
    ↓
Qdrant bağlantısı
Qdrant collection
Embedding modeli
```

## 2. `as_retriever()` ve `invoke()` farkı

`as_retriever()` LangChain'in `QdrantVectorStore` üzerinde hazır gelen metodudur. Vector store'u `BaseRetriever` uyumlu bir nesneye çevirir.

```python
retriever = get_vector_store().as_retriever(
    search_kwargs={
        "k": 30,
        "score_threshold": 0.82,
    }
)
```

Bu satır henüz soru aramaz. Gerçek arama `invoke()` çağrısında başlar:

```python
documents = retriever.invoke("42 mm kapı için hangi vida kullanılmalı?")
```

Arka plandaki semantic akış:

```text
Soru
  ↓
E5 query embedding
  ↓
Qdrant dense vector search
  ↓
Cosine similarity
  ↓
Score threshold ve aday kısıtı
  ↓
Document listesi
```

## 3. Ana product retriever akışı

Dosya:

```text
src/rag/retrievers/product_retriever.py
```

Bu, chatbotun kullandığı ana retrieval giriş noktasıdır:

```text
Kullanıcı sorusu + product_id
        ↓
Qdrant semantic retriever
        +
LangChain BM25Retriever
        ↓
merge_retrieval_candidates()
        ↓
Context expansion
        ↓
CrossEncoder reranker
        ↓
Final top_k Document
```

Ana akışta RRF veya `EnsembleRetriever` kullanılmıyor. Semantic ve BM25 sonuçları ayrı ayrı korunuyor, duplicate'ler temizlenerek aday havuzu oluşturuluyor. Böylece BM25'in bulduğu teknik bir değer, başka kolun sıralaması yüzünden erken aşamada kaybolmuyor.

## 4. Product ID metadata filtresi

Frontend ürün sayfasından şu bilgiyi gönderir:

```json
{
  "question": "42 mm kapı için hangi vida kullanılmalı?",
  "product_id": "SECUREHOME-SHL-500"
}
```

Product retriever bu ID'yi Qdrant payload filtresine uygular:

```text
metadata.product_id == SECUREHOME-SHL-500
```

BM25 kolu da aynı ürünün chunk'larıyla sınırlandırılır. Bu filtre kullanıcının sorusundan ürün adı tahmin etmez; ürün sayfasındaki seçimi kullanır.

## 5. BM25 index

Dosya:

```text
src/rag/retrievers/bm25_index.py
```

BM25 embedding üretmez ve chunk oluşturmaz. Mevcut chunk'ları kelime, sayı ve model kodu eşleşmesine göre sıralar.

```text
Ingestion sırasında:
Markdown → chunk → BM25 index → data/indexes/bm25_retriever.pkl

Sorgu sırasında:
Kullanıcı sorusu → hazır BM25 index → keyword adayları
```

Index her kullanıcı sorusunda yeniden oluşturulmaz. Yeni veya güncellenmiş ürün geldiğinde ingestion çalışır ve index yeniden kaydedilir.

## 6. Context expansion

Dosya:

```text
src/rag/retrievers/context_expander.py
```

Retrieval'ın bulduğu chunk'ın aynı bölümündeki ilişkili chunk'ları aday havuzuna ekler. Bu özellikle teknik tabloların PDF sayfa sınırında bölündüğü durumlarda işe yarar.

## 7. Reranker

Dosya:

```text
src/rag/rerankers/cross_encoder.py
```

`BAAI/bge-reranker-v2-m3` semantic ve BM25 adaylarını soru-belge ilgisine göre yeniden sıralar. Reranker yeni bilgi üretmez; yalnızca mevcut adaylar arasından daha uygun olanı üste taşır.

## 8. Debug retriever'lar

Dosya grubu:

```text
src/rag/retrievers/debug/
```

| Araç | Görevi |
|---|---|
| `qdrant_retriever.py` | Semantic skor, metadata ve Qdrant filtresini gözlemlemek |
| `keyword_retriever.py` | Manuel BM25 skorlarını görmek |
| `hybrid_retriever.py` | Debug amaçlı semantic + BM25 + RRF karşılaştırması yapmak |

Debug hybrid içindeki RRF, ana chatbot akışında kullanılmaz. Yalnızca algoritmik karşılaştırma içindir.

## 9. Güncel test komutları

Semantic Qdrant araması:

```powershell
.venv\Scripts\python.exe -m scripts.search_chunks "42 mm kapı için hangi vida kullanılmalı?" --product-id SECUREHOME-SHL-500
```

Ana production retriever:

```powershell
.venv\Scripts\python.exe -m scripts.search_product_retriever "Piller biterse kilide nasıl güç verilir?"
```

Ürün filtresi olmadan tüm indexi aramak için:

```powershell
.venv\Scripts\python.exe -m scripts.search_product_retriever "kapı kalınlığı" --all-products
```

Manuel BM25:

```powershell
.venv\Scripts\python.exe -m scripts.search_keyword_chunks "54 mm delik çapı" --product-id SECUREHOME-SHL-500
```

Debug hybrid:

```powershell
.venv\Scripts\python.exe -m scripts.search_hybrid_chunks "42 mm kapı vida" --product-id SECUREHOME-SHL-500
```

BM25 index yapısını görmek:

```powershell
.venv\Scripts\python.exe -m scripts.inspect_bm25_index "42 mm kapı"
```

Terim incelemek için:

```powershell
.venv\Scripts\python.exe -m scripts.inspect_bm25_index "vida" --term vida --term 42 --term 54 --term usb-c
```

## 10. Sonuçları nasıl yorumlamalıyız?

- Semantic skor veya BM25 skorları birbirleriyle doğrudan karşılaştırılmaz; farklı ölçekte olabilirler.
- Ana retriever'ın final sıralamasını CrossEncoder reranker belirler.
- En iyi sonuçta ürün ID'si doğru, bölüm metadata'sı anlamlı ve içerik soruyu doğrudan destekliyor olmalıdır.
- Dokümanda olmayan bir soru için doğru davranış, modelin tahmin üretmeyip bilginin kaynakta olmadığını söylemesidir.
- Bir teknik değer ikinci veya üçüncü sıradaysa önce chunk bağlamı, tablo bütünlüğü ve reranker aday havuzu kontrol edilir.

## Kısa özet

```text
get_vector_store()
→ Qdrant vector store'u hazırlar

as_retriever()
→ Vector store'u LangChain retriever arayüzüne çevirir

invoke()
→ Gerçek semantic aramayı başlatır

product_retriever
→ Chatbotun ana semantic + BM25 + context + reranker akışıdır

debug retriever'lar
→ Skorları ve alternatif arama davranışlarını gözlemleme araçlarıdır

RRF
→ Yalnızca debug hybrid karşılaştırmasında vardır; ana akışta yoktur
```
