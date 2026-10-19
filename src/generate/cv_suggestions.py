from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_MODEL
from src.generate.prompts import CV_SUGGESTION_PROMPT

def generate_suggestions(profile: dict, job: str) -> str:
    prompt = CV_SUGGESTION_PROMPT.format(profile=profile, job=job)
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0)
    response = llm.invoke([
        ("system", "You provide evidence-based resume advice."),
        ("human", prompt),
    ])
    return response.content
