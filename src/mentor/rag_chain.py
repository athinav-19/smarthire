from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import CAREER_NOTES_DIR, JOBS_FILE, VECTORSTORE_DIR, GEMINI_MODEL
from src.search.embed import get_embedding_model
from src.safety.guardrails import validate_input

def load_mentor_documents():
    documents = []
    if JOBS_FILE.exists():
        import pandas as pd
        df = pd.read_csv(JOBS_FILE).fillna("")
        for row in df.itertuples():
            documents.append(Document(
                page_content=f"Job: {row.title}\nSkills: {row.skills}\nDescription: {row.description}",
                metadata={"source": "job corpus", "title": row.title},
            ))
    for path in CAREER_NOTES_DIR.glob("*.txt"):
        documents.append(Document(
            page_content=path.read_text(encoding="utf-8"),
            metadata={"source": path.name},
        ))
    return documents

def build_mentor_index():
    documents = load_mentor_documents()
    if not documents:
        raise ValueError("No career notes or job documents were found.")
    store = FAISS.from_documents(documents, get_embedding_model())
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(VECTORSTORE_DIR / "mentor_index"))
    return len(documents)

def load_mentor_index():
    index_path = VECTORSTORE_DIR / "mentor_index"
    if not (index_path.with_suffix(".faiss")).exists():
        build_mentor_index()
    return FAISS.load_local(
        str(index_path),
        get_embedding_model(),
        allow_dangerous_deserialization=True,
    )

def ask_mentor(question: str) -> str:
    allowed, message = validate_input(question)
    if not allowed:
        return message

    docs = load_mentor_index().similarity_search(question, k=4)
    context = "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source', 'document')}\n{doc.page_content}"
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are SmartHire AI Career Mentor.
Answer only using the supplied context.
If the answer is not supported by the context, say:
\"I don't know based on the available career documents.\"
Do not invent facts.

Context:
{context}"""),
        ("human", "{question}"),
    ])
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0)
    result = (prompt | llm).invoke({"context": context, "question": question})
    return result.content
