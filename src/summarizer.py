# Instead of a plain API call, possible parameters that can be added on cmd line:
# length (“short”, “medium”, “detailed”)
# tone (“academic”, “casual”, “bullet-points”)
# Example: python main.py summarize "Your long text here" --length short --tone casual

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads API key from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    # Summarize input text using OpenAI API calls.
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise and clear note summarizer. Provide a summary that captures the main points, but does not leave anything to interpretation."},
                {"role": "user", "content": f"Summarize this text:\n\n{text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
