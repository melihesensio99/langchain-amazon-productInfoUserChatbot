from src.rag.chains.qa_chain import build_answer_chain
from src.rag.retrievers.product_retriever import get_product_retriever
from src.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    """Retrieval ve QA chain'i kullanarak ürün sorularını cevaplar."""

    def __init__(self) -> None:
        # LLM cache'lenir; retriever product_id'ye göre istek içinde seçilir.
        pass

    def answer(self, request: ChatRequest) -> ChatResponse:
        # Ürün sayfasından gelen ID varsa semantic ve keyword aramayı sınırlar.
        retriever = get_product_retriever(request.product_id)
        # Retrieval yalnızca bir kez çalışır; aynı chunk'lar hem kaynak listesine
        # hem de generation prompt'una gönderilir.
        documents = retriever.invoke(request.question)
        answer = build_answer_chain().invoke(
            {
                "question": request.question,
                "documents": documents,
            }
        )
        source_keys: set[tuple] = set()
        sources = []
        for document in documents:
            source = {
                "product_id": document.metadata.get("product_id"),
                "product_name": document.metadata.get("product_name"),
                "source_type": document.metadata.get("source_type"),
                "source_file": document.metadata.get("source_file"),
                "section": document.metadata.get("h2")
                or document.metadata.get("h1"),
            }
            source_key = tuple(source.items())
            if source_key in source_keys:
                continue
            source_keys.add(source_key)
            sources.append(source)
        return ChatResponse(answer=answer, sources=sources)
