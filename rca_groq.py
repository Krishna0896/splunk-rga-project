# rca_groq.py
from groq import APIStatusError


load_dotenv()


GROQ_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


if not GROQ_KEY:
raise RuntimeError("GROQ_API_KEY not set. Add it to your environment or .env file.")


client = Groq(api_key=GROQ_KEY)




def make_prompt(incident_description: str, log_text: str):
prompt = f"""
You are an experienced SRE and Root Cause Analysis specialist.
Produce a concise, structured RCA using this exact format:


1. Incident Summary
2. Business / Technical Impact
3. Timeline (use logs to reconstruct)
4. Immediate Cause
5. Root Cause (perform 5-Whys)
6. Contributing Factors
7. Corrective Actions
8. Preventive Actions


Incident Description:
{incident_description}


Extracted Logs (context):
{log_text}


Be concise, use bullet points where appropriate.
"""
return prompt




def generate_rca(incident_description: str, log_events: list[str]):
# Join logs into a compact string; trim to reasonable length
log_text = "\n".join(log_events)[:6000]
prompt = make_prompt(incident_description, log_text)


try:
resp = client.chat.completions.create(
model=GROQ_MODEL,
messages=[
{"role": "system", "content": "You are an RCA expert."},
{"role": "user", "content": prompt}
],
temperature=0.2
)


# Access message content per Groq SDK
return resp.choices[0].message.content


except APIStatusError as e:
raise RuntimeError(f"Groq API error: {e.status_code} - {getattr(e,'response',e)}")
except Exception as e:
raise RuntimeError(f"Unexpected error: {e}")




if __name__ == "__main__":
# Basic CLI test
incident = input("Incident description:\n")
# Read a small local file of logs for testing
sample_file = 'tests/sample_logs.csv'
from csv_reader import read_csv_logs
logs = read_csv_logs(sample_file)
print(generate_rca(incident, logs[:200]))
