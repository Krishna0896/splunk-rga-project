import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set. Add it to your environment or .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_logs(log_text):
    """
    Send logs to Groq LLM for RCA analysis.
    """
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert SRE performing root cause analysis."},
            {"role": "user", "content": f"Here are the logs:\n{log_text}\n\nProvide RCA."}
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    # Example log text
    logs = """
    ERROR: Database connection failed at 12:04
    WARN: Retrying connection
    ERROR: Max retries exceeded
    """

    print("\n=== RCA OUTPUT ===\n")
    print(analyze_logs(logs))
