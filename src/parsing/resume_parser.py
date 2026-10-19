import json
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_MODEL
from src.parsing.loader import chunk_text

class ResumeProfile(BaseModel):
    name: str = ""
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    target_role: str = ""

PROMPT = '''
Extract a candidate profile from the resume below.

Return ONLY valid JSON with exactly these fields:
name: string
skills: list of strings
experience: list of strings
education: list of strings
target_role: string

Do not invent information. If a field is missing, use an empty string or empty list.

RESUME:
'''

def parse_resume(resume_text: str) -> dict:
    if not resume_text.strip():
        raise ValueError("No readable text was found in the resume.")

    chunks = chunk_text(resume_text)
    prepared_text = "\n\n".join(chunks)

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0,
        google_api_key=None,
        response_mime_type="application/json",
    )
    response = llm.invoke(
        [
            ("system", "You extract resume information accurately."),
            ("human", PROMPT + prepared_text[:20000]),
        ]
    )
    # Gemini may return content as a string or as a list of content blocks.
    content = response.content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
        content = "".join(parts)

    if not isinstance(content, str):
        raise ValueError("Gemini returned an unexpected response format.")

    data = json.loads(content)
    return ResumeProfile.model_validate(data).model_dump()
