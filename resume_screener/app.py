import streamlit as st
import os
from resume_parser import extract_text_from_pdf
from score_resume import score_resume

st.title("🧠 AI-Based Resume Screener")

job_desc = st.text_area("Paste Job Description")

uploaded_files = st.file_uploader("Upload Resumes (PDF)", accept_multiple_files=True, type=['pdf'])

if st.button("Score Resumes"):
    if not job_desc or not uploaded_files:
        st.warning("Please provide a job description and upload at least one resume.")
    else:
        st.subheader("📊 Resume Scores:")
        for file in uploaded_files:
            with open(f"temp_{file.name}", "wb") as f:
                f.write(file.read())

            resume_text = extract_text_from_pdf(resume_path)
            score = score_resume(job_desc, resume_text)
            st.write(f"**{file.name}**: {score} % match")
            os.remove(f"temp_{file.name}")
