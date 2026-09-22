from src.rag.chains.qa_chain import build_qa_chain
from src.rag.retrievers.product_retriever import get_product_retriever
from src.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    """Retrieval ve QA chain'i kullanarak ürün sorularını cevaplar."""

    def __init__(self) -> None:
        # Retriever ilgili chunk'ları, chain ise cevabı üretir.
        self.retriever = get_product_retriever()
        self.chain = build_qa_chain(self.retriever)

    def answer(self, request: ChatRequest) -> ChatResponse:
        documents = self.retriever.invoke(request.question)
        answer = self.chain.invoke({"question": request.question})
        sources = [
            {
                "product_id": document.metadata.get("product_id"),
                "product_name": document.metadata.get("product_name"),
                "source_type": document.metadata.get("source_type"),
                "source_file": document.metadata.get("source_file"),
                "section": document.metadata.get("h2")
                or document.metadata.get("h1"),
            }
            for document in documents
        ]
        return ChatResponse(answer=answer, sources=sources)
