import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("notes.json")  # stored in the same folder for now

def save_note(title: str, text: str, summary: str):
    note = {
        "title": title,
        "text": text,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(note)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)