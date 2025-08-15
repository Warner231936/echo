+18
-0

import json
import time
from typing import List, Dict

LOG_FILE = "lie_log.json"


def log_lie(truth: str, lie: str, original: str) -> None:
    """Record a lie without alerting Requiem."""
    entry = {"time": time.time(), "truth": truth, "lie": lie, "original": original}
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data: List[Dict] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
