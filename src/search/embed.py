from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import GEMINI_EMBEDDING_MODEL

def get_embedding_model():
    return GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL)

def get_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    return get_embedding_model().embed_documents(texts)

def get_embedding(text: str) -> list[float]:
    return get_embedding_model().embed_query(text)
