from langchain_openai import ChatOpenAI
from core.settings import settings

def get_llm(model_name: str = "gpt-4o", temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY
    )

llm = get_llm()
