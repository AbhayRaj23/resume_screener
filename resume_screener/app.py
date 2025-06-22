import streamlit as st
import os
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Title
st.title("📄 AI Resume Screener")
st.write("Upload one or more resumes and compare them with a job description.")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to score resumes
def score_resume(job_desc, resume_text):
    documents = [job_desc, resume_text]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(documents)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(score[0][0]) * 100, 2)  # as percentage

# Job Description Input
job_description = st.text_area("📝 Paste the Job Description here", height=200)

# File Uploader
uploaded_files = st.file_uploader("📤 Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

# Score Button
if st.button("🔍 Score Resumes"):
    if not job_description:
        st.warning("Please enter a job description before scoring.")
    elif not uploaded_files:
        st.warning("Please upload at least one PDF resume.")
    else:
        st.subheader("📊 Resume Match Scores")
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            try:
                resume_text = extract_text_from_pdf(uploaded_file.name)
                score = score_resume(job_description, resume_text)
                st.write(f"**{uploaded_file.name}** → Match Score: `{score}%`")
            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {e}")
            finally:
                os.remove(uploaded_file.name)
