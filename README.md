# SmartHire GenAI

SmartHire GenAI is an intelligent career portal and resume-matching platform powered by Generative AI. It streamlines the job-hunting and career progression workflow by extracting structured profiles from resumes, performing semantic matching against job opportunities, suggesting targeted CV improvements, and offering an interactive AI Career Mentor powered by Retrieval-Augmented Generation (RAG) with built-in safety guardrails.

---

## 🚀 Main Features

- **Resume Parser**: Extracts structured candidate profiles (target role, skills, experience, education) from uploaded PDF and DOCX documents.
- **Semantic Job Search**: Uses dense embeddings to capture the meaning of candidate skills and experience beyond simple keyword matching.
- **FAISS-Based Matching**: Employs FAISS vector indexes to perform fast, scalable vector similarity search across job listings.
- **CV Improvement Generator**: Analyzes candidate profiles against target roles or job descriptions to generate actionable suggestions, highlight missing skills, and provide bullet-point revisions.
- **AI Career Mentor with RAG**: An interactive career advisor answering questions with grounded context retrieved from job descriptions and curated career advisory notes.
- **Guardrails**: Built-in input and output validation that ensures safety and keeps mentor discussions focused strictly on career, technical, and interview topics while preventing prompt injections.
- **Streamlit UI**: A clean, modern, multi-tab web interface designed for end-to-end user interaction.

---

## 🛠️ Technologies Used

- **Python**: Core programming language (3.10+)
- **Gemini API**: State-of-the-art LLMs (`gemini-3.8-flash`) and dense text embeddings (`gemini-embedding-001`) from Google DeepMind
- **LangChain**: RAG orchestration, prompt templates, and vectorstore retrieval pipelines
- **FAISS**: High-performance vector similarity search and index persistence
- **Streamlit**: Interactive web application framework

---

## 📁 Project Structure

```text
smarthire/
├── app/
│   └── streamlit_app.py        # Streamlit web application interface
├── data/
│   ├── career_notes/           # Curated domain knowledge for RAG mentor
│   ├── jobs/                   # Job listings dataset (jobs.csv)
│   └── resumes/                # Uploaded resumes (ignored in git)
├── notebooks/                  # Prototyping and exploration notebooks
├── reports/                    # Quality evaluations and report documents
├── src/
│   ├── generate/               # CV suggestion generation and prompt logic
│   ├── mentor/                 # RAG chain implementation for career mentor
│   ├── parsing/                # Document loaders and LLM-based resume parser
│   ├── safety/                 # Guardrails and topic validation
│   ├── search/                 # Embedding utilities and FAISS job search
│   ├── config.py               # Central configuration and paths
│   └── evaluate.py             # Evaluation module for retrieval and mentor responses
├── vectorstore/                # Local FAISS index storage (ignored in git)
├── .env.example                # Example environment variable configuration
├── .gitignore                  # Git ignore rules for secrets and generated files
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

---

## ⚙️ Installation and Run Instructions

### 1. Prerequisites
- Python 3.10+ installed
- A Google Gemini API key

### 2. Clone the Repository
```bash
git clone https://github.com/athinav-19/smarthire.git
cd smarthire
```

### 3. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (cmd / powershell):
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variable Setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env     # Linux / macOS
copy .env.example .env   # Windows
```

Edit `.env` and fill in your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

> **Security Note:** Never commit or expose your `.env` file or actual API keys. `.env` is ignored by `.gitignore`.

### 6. Run the Application
Launch the Streamlit dashboard:
```bash
streamlit run app/streamlit_app.py
```

The application will automatically build the FAISS index on first run if it does not already exist.

---

## 📄 License
This project is open-source under the MIT License.