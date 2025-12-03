# splunk_fetch.py
import os
from dotenv import load_dotenv
import splunklib.client as client
import splunklib.results as results


load_dotenv()


SPLUNK_HOST = os.getenv("SPLUNK_HOST", "localhost")
SPLUNK_PORT = int(os.getenv("SPLUNK_PORT", 8089))
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME")
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD")
SPLUNK_VERIFY = os.getenv("SPLUNK_VERIFY_SSL", "False").lower() in ("true", "1", "yes")




def fetch_splunk_logs(search_query: str, count: int = 500):
"""Connect to Splunk and fetch results for a search query."""
service = client.connect(
host=SPLUNK_HOST,
port=SPLUNK_PORT,
username=SPLUNK_USERNAME,
password=SPLUNK_PASSWORD,
scheme="https" if SPLUNK_VERIFY else "http"
)


job = service.jobs.create(search_query, exec_mode="blocking", count=count)
reader = results.ResultsReader(job.results())


logs = []
for item in reader:
if isinstance(item, dict):
# Use _raw if present, else the fields
raw = item.get("_raw") or str(item)
logs.append(raw)


return logs




if __name__ == "__main__":
# Quick test
q = f"search index={os.getenv('SPLUNK_INDEX','mylogs')} | head 100"
logs = fetch_splunk_logs(q)
print("Fetched", len(logs), "events")
for l in logs[:10]:
print(l)
