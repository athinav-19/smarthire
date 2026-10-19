import json
import pandas as pd
from langchain_community.vectorstores import FAISS
from src.config import JOBS_FILE, VECTORSTORE_DIR, TOP_K
from src.search.embed import get_embedding_model

def load_jobs():
    if not JOBS_FILE.exists():
        raise FileNotFoundError(f"Job dataset not found: {JOBS_FILE}")
    df = pd.read_csv(JOBS_FILE).fillna("")
    required = {"title", "skills", "description"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"jobs.csv is missing columns: {', '.join(missing)}")
    return df

def build_job_index():
    df = load_jobs()
    texts = [
        f"Job title: {row.title}\nSkills: {row.skills}\nDescription: {row.description}"
        for row in df.itertuples()
    ]
    store = FAISS.from_texts(texts, get_embedding_model())
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(VECTORSTORE_DIR / "jobs_index"))
    with open(VECTORSTORE_DIR / "jobs_metadata.json", "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)
    return len(df)

def load_job_index():
    index_path = VECTORSTORE_DIR / "jobs_index"
    if not (index_path.with_suffix(".faiss")).exists():
        build_job_index()
    return FAISS.load_local(
        str(index_path),
        get_embedding_model(),
        allow_dangerous_deserialization=True,
    )

def search_jobs(profile: dict, top_k: int = TOP_K):
    query = (
        f"Target role: {profile.get('target_role', '')}\n"
        f"Skills: {', '.join(profile.get('skills', []))}\n"
        f"Experience: {'; '.join(profile.get('experience', []))}"
    )
    results = load_job_index().similarity_search_with_score(query, k=top_k)
    return [{"job": doc.page_content, "score": round(float(score), 4)} for doc, score in results]
