from langchain_groq import ChatGroq

from core.config import settings


if not settings.GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set in the .env file."
    )


llm = ChatGroq(
    model=settings.GROQ_MODEL,
    temperature=0.2,
    api_key=settings.GROQ_API_KEY,
)