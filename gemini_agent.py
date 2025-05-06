import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the .env file and configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_affirmation(mood: str) -> str:
    model = genai.GenerativeModel("models/gemma-3-27b-it")
    prompt = f"Give me only a short, clear affirmation (1–2 lines) for someone who feels {mood.lower()}."

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Clean and extract affirmation
    cleaned = (
        raw.replace('\n', ' ')
           .replace('\\', '')
           .replace('\"', '"')
           .replace('*', '')
           .strip(" “”\"'")
    )

    # Remove preamble if present
    if ":" in cleaned:
        cleaned = cleaned.split(":", 1)[-1].strip()

    return cleaned