import json
import os

LOG_FILE = "logs.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_log(entry):
    data = load_logs()
    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)