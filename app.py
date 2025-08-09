import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv(st.secrets["GOOGLE_API_KEY"]))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text


input_prompt = """
Hey, act like a highly skilled and experienced ATS (Applicant Tracking System) with deep expertise in software engineering, data science, data analysis, and big data engineering. Your job is to evaluate the given resume against the provided job description in the context of a highly competitive job market. You must provide the most accurate analysis possible, including: 
1) JD Match percentage based on skills, experience, and keywords.
2) Missing keywords that are critical for ATS ranking.
3) A concise profile summary with suggestions for improvement.

Return the response strictly as one single JSON-formatted string with no extra text, using this exact structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}

Resume: {text}
Description: {jd}
"""

st.title("Smart ATS")
st.write("Improve Your Resume for ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        final_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(final_prompt)
        st.write(response)
