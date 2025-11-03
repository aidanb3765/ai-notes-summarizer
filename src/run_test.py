from pathlib import Path
from summarizer import summarize_text

file = Path("test.txt")  # test.txt is in the same folder
text = file.read_text(encoding="utf-8")

summary = summarize_text(text)

print("\nSummary:\n")
print(summary)
print("\nOriginal Text:\n")
print(text)