import re

from langchain_core.output_parsers import StrOutputParser

from src.rag.llm import get_llm
from src.rag.prompts.product_qa import PRODUCT_QA_PROMPT


def format_documents(documents) -> str:
    """Retrieval sonucu Document listesini prompt bağlamına çevirir."""
    return "\n\n".join(document.page_content for document in documents)


def clean_answer(answer: str) -> str:
    """Modelin Markdown biçimlendirmesini düz metne çevirir."""
    # Cevapların frontend'de doğal görünmesi için kalın/italik işaretlerini,
    # backtick'leri ve Markdown başlık işaretlerini kaldırıyoruz.
    answer = re.sub(r"[*`]", "", answer)
    answer = re.sub(r"(?m)^\s*#+\s*", "", answer)
    return answer.strip()


def build_answer_chain():
    """Hazır retrieval sonuçlarını Mistral ile cevaba dönüştüren zincir."""
    return (
        {
            "context": lambda value: format_documents(value["documents"]),
            "question": lambda value: value["question"],
        }
        | PRODUCT_QA_PROMPT
        | get_llm()
        | StrOutputParser()
        | clean_answer
    )
