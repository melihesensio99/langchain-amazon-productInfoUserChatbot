from src.rag.chains.qa_chain import build_qa_chain
from src.rag.retrievers.product_retriever import get_product_retriever
from src.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self) -> None:
        self.retriever = get_product_retriever()
        self.chain = build_qa_chain(self.retriever)

    def answer(self, request: ChatRequest) -> ChatResponse:
        documents = self.retriever.invoke(request.question)
        answer = self.chain.invoke({"question": request.question})
        sources = [
            {
                "document_id": document.metadata.get("document_id"),
                "baslik": document.metadata.get("baslik"),
                "icerik_turu": document.metadata.get("icerik_turu"),
            }
            for document in documents
        ]
        return ChatResponse(answer=answer, sources=sources)
