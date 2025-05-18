import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Validate
if not api_key:
    raise ValueError("❌ Missing GEMINI_API_KEY in environment variables")

# Configure Gemini
genai.configure(api_key=api_key)

# Generate mood-based affirmation
def generate_affirmation(mood: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Give me only a short, clear affirmation (1–2 lines) for someone who feels {mood.lower()}."
    response = model.generate_content(prompt)

    raw = response.text.strip()
    cleaned = (
        raw.replace('\n', ' ')
           .replace('\\', '')
           .replace('\"', '"')
           .replace('*', '')
           .strip(" “”\"'")
    )
    if ":" in cleaned:
        cleaned = cleaned.split(":", 1)[-1].strip()

    return cleaned
