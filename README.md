# splunk-rga-project

STEP 1 — Start a Local Splunk Instance (Free Trial)
Option A — Download Splunk Enterprise (GUI version)

Go to: https://www.splunk.com/en_us/download/splunk-enterprise.html

Download → Install

Start Splunk:

http://localhost:8000


Login (default):

Username: admin

Password: the one you set during installation

Ensure the Splunk management port 8089 is enabled (this is important because your Python script connects via port 8089).

✅ STEP 2 — Index Sample Logs into Splunk

You need logs inside Splunk so the Groq RCA generator can fetch them.

Method 1 — Upload a CSV Log File

Go to:

Settings → Add Data


Choose:

Upload File

Upload your sample log file (you can use the sample_logs.csv from the project).

Choose Create New Index → name it:

mylogs


Finish.

Splunk will parse the logs and index them.

✅ STEP 3 — Verify Logs Using a Search Query

Go to:

Search & Reporting


Run:

search index=mylogs | head 20


If you see logs → 👍 Splunk side is ready.

✅ STEP 4 — Configure Your .env File

Inside your project folder, edit .env:

SPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=YOURPASSWORD
SPLUNK_VERIFY_SSL=False
SPLUNK_INDEX=mylogs

GROQ_API_KEY=gsk_.....
GROQ_MODEL=llama-3.1-8b-instant

✅ STEP 5 — Test Using splunk_fetch.py

Run:

python splunk_fetch.py


If successful you will see:

Fetched 4 events
ERROR: DB connection timeout
WARN: retrying connection
...


If you see this → Splunk connection works correctly.

✅ STEP 6 — Test the RCA Pipeline (CLI)

Run:

python rca_groq.py


Enter any incident description when prompted:

Database outage affecting user login


If everything is correct → you will get a complete RCA:

1. Incident Summary  
2. Impact  
3. Timeline (reconstructed from logs)  
4. Immediate Cause  
5. Root Cause  
6. Fix  
7. Preventive Actions  

✅ STEP 7 — Test Using Streamlit Web UI

Start the GUI:

streamlit run app_streamlit.py


The UI will open in browser → http://localhost:8501

Choose:

Input source → Fetch from Splunk


Enter search:

search index=mylogs | head 100


Click:

[Fetch logs]
[Generate RCA]



1. Load Groq API + Environment Setup
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

✔ Purpose

Load your API key

Allow secure authentication

Prevent hard-coding your key in the script

🔹 2. Create Groq Client
client = Groq(api_key=api_key)

✔ Purpose

This creates a connection to Groq’s LLMs so you can send data to the AI model.

🔹 3. Build Prompt for RCA (This is the Core AI Logic!)
prompt = f"""
You are an expert in Root Cause Analysis (RCA).
Analyze the following logs and generate a structured RCA:

LOGS:
{logs}
"""

✔ Purpose

You tell the model:

What role it should play → "expert in RCA"

What data to analyze → the logs

What format you expect → structured RCA

This is why the AI gives you:

Symptoms

Timeline

Root cause

Corrective actions

🔹 4. Call the Groq Model
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

✔ Purpose

This sends your logs to the LLM and generates an RCA.

Why temperature=0.2?

Low temperature → predictable → professional RCA output.

🔹 5. Extract AI Response
return completion.choices[0].message.content

✔ Purpose

This extracts only the final RCA text from Groq’s response.

🔹 6. Prints Final RCA
print(analyze_logs(logs))


You see something like:

Root Cause: Database connection failure due to...
Corrective Actions: Implement monitoring...

🎯 Full Flow of RCA via Gen AI (Clear Summary)

Here is the full process your code performs:

Logs → Format into prompt → Send to Groq LLM → AI analyzes patterns →
AI identifies root cause → AI generates RCA → Output to user

🔥 Why This Works So Well

Your Gen-AI RCA system works because:

✔ The model sees real logs

Time + service + message → patterns become obvious.

✔ LLM recognizes error sequences

Example:

Retry → Timeout → Failure → Root cause = network latency


You'll see:

The RCA

Download PDF button
