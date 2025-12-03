# app_streamlit.py
import os
from dotenv import load_dotenv
import streamlit as st
from splunk_fetch import fetch_splunk_logs
from csv_reader import read_csv_logs, read_excel_logs
from rca_groq import generate_rca
from save_pdf import save_text_pdf


load_dotenv()


st.title("RCA Generator — Splunk / CSV → Groq")


source = st.selectbox("Input source:", ["Manual text", "Upload CSV", "Upload Excel", "Fetch from Splunk"])


incident = st.text_input("Incident description")


logs = []


if source == "Upload CSV":
f = st.file_uploader("Upload CSV file", type=["csv"])
if f:
logs = read_csv_logs(f)
elif source == "Upload Excel":
f = st.file_uploader("Upload Excel file", type=["xlsx"])
if f:
logs = read_excel_logs(f)
elif source == "Fetch from Splunk":
query = st.text_area("Splunk search query", value=f"search index={os.getenv('SPLUNK_INDEX','mylogs')} | head 200")
if st.button("Fetch logs"):
with st.spinner("Fetching logs from Splunk..."):
logs = fetch_splunk_logs(query)
else:
logs = []


if st.button("Generate RCA"):
if not incident.strip() and not logs:
st.error("Enter incident description or provide logs")
else:
with st.spinner("Generating RCA..."):
rca_text = generate_rca(incident, logs or [])
st.subheader("Generated RCA")
st.text(rca_text)


# PDF download
pdf_file = save_text_pdf(rca_text, filename="rca_output.pdf")
with open(pdf_file, "rb") as fh:
st.download_button("Download PDF", fh, file_name=pdf_file)
