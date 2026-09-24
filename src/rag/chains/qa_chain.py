from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from src.rag.llm import get_llm
from src.rag.prompts.product_qa import PRODUCT_QA_PROMPT


def build_qa_chain(retriever):
    def format_docs(documents):
        return "\n\n".join(document.page_content for document in documents)

    # Retriever yalnızca soru metnini almalı; QA zincirinin sözlüğünü değil.
    # Aksi halde BM25 tokenizer, {"question": ...} sözlüğünde .lower() çağırmaya
    # çalışır ve üretim isteği 500 ile sonuçlanır.
    context_retriever = RunnableLambda(lambda value: value["question"]) | retriever | format_docs

    return (
        {"context": context_retriever, "question": lambda value: value["question"]}
        | PRODUCT_QA_PROMPT
        | get_llm()
        | StrOutputParser()
    )
