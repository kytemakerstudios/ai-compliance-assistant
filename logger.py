import json
from datetime import datetime

LOG_FILE = "logs/interactions.jsonl"

def log_interaction(query, response):
    log = {
        "timestamp": str(datetime.utcnow()),
        "query": query[:200],
        "risk_level": response.get("risk_level"),
        "sources": response.get("sources")
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")
