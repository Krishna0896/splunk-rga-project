import requests
import json

# Disable warnings for self-signed certificates (only for local Splunk)
requests.packages.urllib3.disable_warnings()


def fetch_splunk_logs(search_query):
    """Connect to Splunk and fetch results for a search query."""
    
    splunk_host = "https://localhost:8089"
    username = "admin"
    password = "Mornemorkel@1996"   # change this

    # Splunk search job endpoint
    search_url = f"{splunk_host}/services/search/jobs"

    # Splunk authentication
    auth = (username, password)

    # Submit search job
    data = {
        "search": f"search {search_query}",
        "exec_mode": "blocking",
        "output_mode": "json"
    }

    response = requests.post(search_url, auth=auth, data=data, verify=False)

    if response.status_code != 201:
        print("Error creating search job:", response.text)
        return []

    sid = response.json()['sid']

    # Fetch results
    results_url = f"{splunk_host}/services/search/jobs/{sid}/results"

    results_response = requests.get(results_url, auth=auth, params={"output_mode": "json"}, verify=False)

    if results_response.status_code != 200:
        print("Error fetching results:", results_response.text)
        return []

    result_data = results_response.json()

    # Extract events
    events = []
    for row in result_data["results"]:
        events.append(row)

    return events


# Simple test call
if __name__ == "__main__":
    logs = fetch_splunk_logs("index=mylogs | head 5")
    print(json.dumps(logs, indent=2))
