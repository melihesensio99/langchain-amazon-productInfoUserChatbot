# Retriever Notları

Bu dosya, retrieval katmanında karışabilecek kavramları ve mevcut akışı açıklar.

## 1. `get_vector_store()` ne yapar?

`get_vector_store()` bizim yazdığımız yardımcı/factory fonksiyonudur.

```python
def get_vector_store() -> QdrantVectorStore:
    settings = get_settings()
    ensure_collection()

    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=settings.qdrant_collection,
        embedding=get_embeddings(),
    )
```

Bu fonksiyon henüz arama yapmaz. Sadece şunları hazırlar:

```text
Qdrant bağlantısı
Qdrant collection'ı
Embedding modeli
```

Sonuç olarak bir `QdrantVectorStore` nesnesi döndürür.

## 2. `as_retriever()` ne yapar?

`as_retriever()` bizim yazdığımız bir fonksiyon değildir. `QdrantVectorStore` sınıfının LangChain'den gelen hazır metodudur.

```python
store = get_vector_store()
retriever = store.as_retriever(
    search_kwargs={
        "k": settings.top_k,
        "score_threshold": settings.retrieval_score_threshold,
    }
)
```

Bu satır arama yapmaz; vector store'u LangChain'in kullanabileceği retriever arayüzüne çevirir.

Gerçek arama şu çağrıda yapılır:

```python
documents = retriever.invoke("iPhone 14 kaç gram?")
```

Arka planda kabaca şu akış gerçekleşir:

```text
invoke(question)
→ query embedding
→ Qdrant similarity search
→ cosine similarity
→ score threshold
→ top_k chunk
```

## 3. Default arama türümüz nedir?

Şu anki `QdrantVectorStore` kullanımımızda default arama semantic/dense vector search'tür.

Sebebi:

```python
embedding=get_embeddings()
```

ile embedding modeli bağlanıyor ve Qdrant dense vector'lar üzerinden arama yapıyor.

Mevcut akış:

```text
Kullanıcı sorusu
→ multilingual-e5-small query embedding
→ Qdrant dense vector search
→ cosine similarity
→ top_k ve score threshold
→ chunk'lar
```

BM25 veya sparse search Qdrant'ın default araması değildir; ancak ana product retriever akışında ayrıca LangChain `BM25Retriever` ile çalıştırılır.

## 4. `product_retriever.py` ne yapar?

Dosya:

```text
src/rag/retrievers/product_retriever.py
```

Chatbot'un kullandığı ana retriever giriş noktasıdır.

```python
def get_product_retriever():
    settings = get_settings()
    return get_vector_store().as_retriever(
        search_kwargs={
            "k": settings.top_k,
            "score_threshold": settings.retrieval_score_threshold,
        }
    )
```

Chat service bu retriever'ı chain'e verir:

```text
ChatService
→ product_retriever
→ QA chain
→ LLM
```

`product_retriever.py` semantic search kodunu satır satır yazmaz; hazır LangChain retriever bileşenlerini chain'e bağlar. İçeride Qdrant semantic retriever ile `BM25Retriever`'ı `EnsembleRetriever` üzerinden birleştirir.

## 5. `qdrant_retriever.py` ne yapar?

Dosya:

```text
src/rag/retrievers/debug/qdrant_retriever.py
```

Bu dosya manuel test ve debug içindir.

```python
get_vector_store().similarity_search_with_score(
    query,
    k=limit,
    filter=query_filter,
    score_threshold=threshold,
)
```

Sonuçları skorları ve metadata bilgileriyle açıkça görmemizi sağlar.

İki dosya birbirini çağırmaz:

```text
product_retriever.py
→ chatbotun kullandığı retriever

qdrant_retriever.py
→ manuel arama, skor ve metadata test aracı
```

İkisi de aynı `get_vector_store()` fonksiyonunu ve aynı Qdrant collection'ını kullanır.

## 6. `keyword_retriever.py` ne yapar?

Dosya:

```text
src/rag/retrievers/debug/keyword_retriever.py
```

Bu dosya BM25 keyword aramasını prototip olarak çalıştırır.

```text
Markdown
→ chunk
→ kelimelere ayırma
→ BM25 index
→ sorgu kelimeleriyle eşleştirme
→ keyword skoru
```

Bu dosyadaki özel `BM25Okapi` prototipi chatbotun ana retriever'ına bağlı değildir; manuel skor testi için kullanılır. Ana akışta LangChain'in hazır `BM25Retriever` bileşeni kullanılır:

```powershell
python -m scripts.search_keyword_chunks "iPhone 14 kapasite 128 GB"
```

BM25 semantic embedding üretmez ve chunk oluşturmaz. Mevcut chunk'ları kelime bazında sıralar.

Ana akışta BM25 index'i ingestion sırasında oluşturulur ve `data/indexes/bm25_retriever.pkl` dosyasına kaydedilir. Sorgu geldiğinde bu hazır index yüklenir; her sorguda Markdown'lar tekrar okunup index kurulmaz.

### BM25 index neden diske kaydedilir?

Server hiç kapanmıyor gibi görünse bile production ortamında şu olaylar yaşanabilir:

```text
Server crash
Deployment
Docker container restart
Makine restart
Worker process restart
```

Index yalnızca RAM'de tutulursa bu olaylarda kaybolur. Bu nedenle ingestion sırasında index diske yazılır:

```text
Ingestion:
chunk'lar → BM25 index → data/indexes/bm25_retriever.pkl

Server başlangıcı:
dosyadan BM25 index'i RAM'e yükle

Kullanıcı sorgusu:
RAM'deki hazır index'i kullan
```

Index her kullanıcı sorusunda yeniden oluşturulmaz. Yeni ürün veya güncellenmiş doküman geldiğinde ingestion tekrar çalışır ve index dosyası güncellenir.

Production'da daha büyük sistemlerde bu yerel pickle dosyası yerine Qdrant sparse index'i, Elasticsearch/OpenSearch veya paylaşılan persistent storage kullanılabilir.

## 7. Mevcut hybrid yapı

Dışarıya yine tek bir `product_retriever` sunuyoruz; içeride LangChain'in hazır bileşenleriyle iki arama yöntemi çalışıyor:

```text
product_retriever
    ↓
EnsembleRetriever
    ├── Qdrant semantic/dense retriever
    └── LangChain BM25Retriever
    ↓
birleştirilmiş ve yeniden sıralanmış chunk'lar
```

Chatbot semantic mi, BM25 mi kullanıldığını bilmek zorunda değil.

`EnsembleRetriever` sonuç sıralarını RRF benzeri rank fusion ile birleştirir. Çünkü cosine similarity ve BM25 skorları aynı ölçekte değildir.

## Kısa özet

```text
get_vector_store()
→ Qdrant vector store nesnesini hazırlar

as_retriever()
→ vector store'u LangChain retriever'ına çevirir

invoke()
→ gerçek semantic search'ü başlatır

product_retriever
→ chatbotun ana retriever arayüzüdür

qdrant_retriever
→ manuel semantic search ve metadata filter test aracıdır

keyword_retriever
→ manuel BM25 skor testi için özel prototiptir

hybrid_retriever
→ manuel özel hybrid prototipidir; ana akışta hazır `EnsembleRetriever` kullanılır
```
