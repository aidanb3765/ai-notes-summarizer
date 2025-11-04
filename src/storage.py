import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("notes.json")

def _load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def save_note(title: str, text: str, summary: str):
    note = {
        "title": title,
        "text": text,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }
    data = _load_data()
    data.append(note)
    _save_data(data)

def list_notes():
    return _load_data()

def get_note(title: str):
    data = _load_data()
    for note in data:
        if note["title"].lower() == title.lower():
            return note
    return None

def delete_note(title: str):
    """Delete a note by title, with selection if multiple exist."""
    notes = load_notes()
    matches = [n for n in notes if title.lower() in n["title"].lower()]

    if not matches:
        print(f"No notes found with title '{title}'.")
        return

    if len(matches) == 1:
        confirm = input(f"Delete '{matches[0]['title']}' ({matches[0]['timestamp']})? (y/n): ").strip().lower()
        if confirm == "y":
            notes.remove(matches[0])
            save_notes(notes)
            print("Note deleted.")
        return

    print(f"\nMultiple notes found for '{title}':")
    for idx, note in enumerate(matches, 1):
        print(f"{idx}. {note['title']} ({note['timestamp']})")

    choice = input("\nEnter the number of the note to delete (or press Enter to cancel): ").strip()
    if not choice.isdigit() or int(choice) not in range(1, len(matches) + 1):
        print("Canceled.")
        return

    note_to_delete = matches[int(choice) - 1]
    notes.remove(note_to_delete)
    save_notes(notes)
    print(f"Deleted '{note_to_delete['title']}' ({note_to_delete['timestamp']}).")

def search_notes(keyword: str):
    data = _load_data()
    keyword = keyword.lower()
    return [
        n for n in data
        if keyword in n["title"].lower() or keyword in n["summary"].lower()
    ]