#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install python-dotenv
# !pip install google-cloud-language
# !pip install PyPDF2
# !pip install docx
# !pip install --upgrade python-docx
# !pip install --upgrade openai


# In[2]:


import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
from openai import OpenAI
import anthropic
import re


# In[3]:


# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


# In[4]:


# Initialize API clients

openai_client = OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# In[5]:


# File parsing

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type == "text/plain":
        return extract_text_from_txt(file)
    else:
        st.error("Unsupported file format.")
        return None


# In[6]:


# LLM Match Analysis

def analyze_with_openai(resume_text, job_desc_text):
    prompt = f"""
    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    Match this resume to the job description. Provide percentage scores in this format:
    - Skills: XX%
    - Experience: XX%
    - Education: XX%
    - Overall: XX%

    Then explain the match.
    """
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a resume-job match evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def analyze_with_anthropic(resume_text, job_desc_text):
    prompt = f"""
    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    Match this resume to the job. Provide match percentages in this format:
    - Skills: XX%
    - Experience: XX%
    - Education: XX%
    - Overall: XX%

    Then briefly explain the match.
    """
    response = anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text.strip()


# In[7]:


# Utility functions

def extract_scores(text):
    scores = {"Skills": "N/A", "Experience": "N/A", "Education": "N/A", "Overall": "N/A"}
    pattern = r"-\s*(Skills|Experience|Education|Overall)\s*:\s*(\d{1,3})\s*%"
    matches = re.findall(pattern, text, re.IGNORECASE)
    for category, value in matches:
        scores[category.capitalize()] = f"{value}%"
    return scores

def display_section(title, left_text, right_text):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 🤖 OpenAI – {title}")
        st.markdown(left_text or "_Not provided_", unsafe_allow_html=True)
    with col2:
        st.markdown(f"### 🧠 Claude – {title}")
        st.markdown(right_text or "_Not provided_", unsafe_allow_html=True)


# In[8]:


# Streamlit App

st.set_page_config(page_title="Resume Match Analyzer", layout="centered")
st.title("🧠 Resume and Job Description Match Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
job_desc_file = st.file_uploader("Upload Job Description (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if resume_file and job_desc_file:
    resume_text = extract_text(resume_file)
    job_desc_text = extract_text(job_desc_file)

    if resume_text and job_desc_text:
        if st.button("Analyze") or "results" in st.session_state:
            if "results" not in st.session_state:
                openai_output = analyze_with_openai(resume_text, job_desc_text)
                claude_output = analyze_with_anthropic(resume_text, job_desc_text)
                st.session_state.results = {
                    "OpenAI": openai_output,
                    "Claude": claude_output
                }
            else:
                openai_output = st.session_state.results["OpenAI"]
                claude_output = st.session_state.results["Claude"]

            openai_scores = extract_scores(openai_output)
            claude_scores = extract_scores(claude_output)

            def to_num(score): return int(score.replace('%', '')) if '%' in score else 0
            openai_overall = to_num(openai_scores.get("Overall", "0%"))
            claude_overall = to_num(claude_scores.get("Overall", "0%"))

            st.markdown("## 📈 Match Score Comparison (%)")
            score_table = {
                "Criteria": ["Skills", "Experience", "Education", "Overall"],
                "OpenAI": [openai_scores["Skills"], openai_scores["Experience"], openai_scores["Education"], openai_scores["Overall"]],
                "Claude": [claude_scores["Skills"], claude_scores["Experience"], claude_scores["Education"], claude_scores["Overall"]]
            }
            st.table(score_table)

            if openai_overall < 95 or claude_overall < 95:
                if st.button("🔧 Show CV Improvement Suggestions"):
                    openai_prompt = f"""
                    Resume Analysis from OpenAI:
                    {openai_output}

                    Based on this, suggest detailed, actionable improvements to make the resume stronger and improve match scores.
                    """

                    claude_prompt = f"""
                    Resume Analysis from Claude:
                    {claude_output}

                    Based on this, suggest detailed, actionable improvements to make the resume stronger and improve match scores.
                    """

                    openai_response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": openai_prompt}],
                        temperature=0.7,
                        max_tokens=600
                    ).choices[0].message.content.strip()

                    claude_response = anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=800,
                        temperature=0.7,
                        messages=[{"role": "user", "content": claude_prompt}]
                    ).content[0].text.strip()

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🤖 OpenAI Suggestions")
                        st.markdown(openai_response)

                    with col2:
                        st.markdown("### 🧠 Claude Suggestions")
                        st.markdown(claude_response)

            if st.button("📊 Show Resume Match Comparison"):
                st.markdown("## 🧩 Detailed Comparison")
                display_section("OpenAI Output", openai_output, claude_output)


# In[ ]:




