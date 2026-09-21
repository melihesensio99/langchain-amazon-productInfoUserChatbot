from langchain_core.output_parsers import StrOutputParser

from src.rag.llm import get_llm
from src.rag.prompts.product_qa import PRODUCT_QA_PROMPT


def build_qa_chain(retriever):
    def format_docs(documents):
        return "\n\n".join(document.page_content for document in documents)

    return (
        {"context": retriever | format_docs, "question": lambda value: value["question"]}
        | PRODUCT_QA_PROMPT
        | get_llm()
        | StrOutputParser()
    )
