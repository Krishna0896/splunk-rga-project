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


You'll see:

The RCA

Download PDF button
