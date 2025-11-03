import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads API key from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    """
    Summarize input text using OpenAI API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise and clear note summarizer."},
                {"role": "user", "content": f"Summarize this text:\n\n{text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
