# todo/storage.py

import json
import os

FILE = "tasks.json"

def load():
    if os.path.exists(FILE) and os.path.getsize(FILE) > 0:
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f)
