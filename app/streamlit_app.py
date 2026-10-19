import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.config import check_api_key
from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.job_search import search_jobs
from src.generate.cv_suggestions import generate_suggestions
from src.mentor.rag_chain import ask_mentor

st.set_page_config(page_title="SmartHire GenAI", page_icon="💼", layout="wide")
st.title("SmartHire GenAI")
st.caption("Resume Matching & AI Career Mentor")

if not check_api_key():
    st.error("GEMINI_API_KEY is missing. Copy .env.example to .env and add your Gemini API key.")
    st.stop()

if "profile" not in st.session_state:
    st.session_state.profile = None
if "matches" not in st.session_state:
    st.session_state.matches = []

tab1, tab2, tab3, tab4 = st.tabs(
    ["Resume Parser", "Job Matches", "CV Improvement", "AI Career Mentor"]
)

with tab1:
    st.subheader("Upload Resume")
    uploaded = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    if uploaded and st.button("Parse Resume"):
        with st.spinner("Reading resume..."):
            try:
                text = load_resume(uploaded.getvalue(), uploaded.name)
                st.session_state.profile = parse_resume(text)
                st.success("Resume parsed successfully.")
            except Exception as e:
                st.error(str(e))
    if st.session_state.profile:
        st.json(st.session_state.profile)

with tab2:
    st.subheader("Semantic Job Search")
    if not st.session_state.profile:
        st.info("Parse a resume first.")
    elif st.button("Find Matching Jobs"):
        with st.spinner("Searching jobs..."):
            try:
                st.session_state.matches = search_jobs(st.session_state.profile)
            except Exception as e:
                st.error(str(e))
    for i, item in enumerate(st.session_state.matches, 1):
        st.markdown(f"### {i}. Match")
        st.write(item["job"])
        st.caption(f"Similarity distance: {item['score']}")

with tab3:
    st.subheader("CV Improvement Generator")
    if not st.session_state.profile:
        st.info("Parse a resume first.")
    else:
        default_job = st.session_state.matches[0]["job"] if st.session_state.matches else ""
        job = st.text_area("Target job description", value=default_job, height=180)
        if st.button("Generate Suggestions"):
            if not job.strip():
                st.warning("Enter a target job description.")
            else:
                with st.spinner("Generating advice..."):
                    try:
                        st.markdown(generate_suggestions(st.session_state.profile, job))
                    except Exception as e:
                        st.error(str(e))

with tab4:
    st.subheader("AI Career Mentor")
    st.write("Ask questions about careers, resumes, jobs, skills, and interviews.")
    question = st.chat_input("Ask a career question...")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Searching career documents..."):
                try:
                    st.write(ask_mentor(question))
                except Exception as e:
                    st.error(str(e))
