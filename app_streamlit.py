import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Add it to .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


def generate_rca(log_text):
    prompt = f"""
    Perform a detailed Root Cause Analysis on the following logs:

    logs:
    {log_text}

    Provide output in this format:
    - Summary
    - Root Cause
    - Impact
    - Timeline of Events
    - Recommended Fix
    - Preventive Actions
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return completion.choices[0].message.content


st.title("🔍 AI-Powered RCA Generator (Groq + Streamlit)")

uploaded_file = st.file_uploader("Upload CSV log file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 📄 Loaded Log File:")
    st.dataframe(df)

    # Convert DataFrame to plain text logs
    log_text = "\n".join(
        df.astype(str).apply(lambda row: ", ".join(row.values), axis=1)
    )

    if st.button("Generate RCA"):
        with st.spinner("Analyzing logs using Groq..."):
            rca_result = generate_rca(log_text)

        st.write("### 🧠 RCA Output")
        st.success(rca_result)
