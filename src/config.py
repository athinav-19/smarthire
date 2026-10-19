import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

DATA_DIR = ROOT_DIR / "data"
JOBS_FILE = DATA_DIR / "jobs" / "jobs.csv"
CAREER_NOTES_DIR = DATA_DIR / "career_notes"
VECTORSTORE_DIR = ROOT_DIR / "vectorstore"

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
TOP_K = 5

def check_api_key():
    return bool(os.getenv("GEMINI_API_KEY"))
