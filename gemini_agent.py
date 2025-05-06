import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (for local dev)
load_dotenv()

# Prefer GOOGLE_API_KEY or fallback to GEMINI_API_KEY
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Raise error if missing
if not api_key:
    raise ValueError("❌ No API key found. Set GOOGLE_API_KEY in Render or GEMINI_API_KEY in .env.")

# Configure Gemini
genai.configure(api_key=api_key)

def generate_affirmation(mood: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = f"Give me only a short, clear affirmation (1–2 lines) for someone who feels {mood.lower()}."
    response = model.generate_content(prompt)

    # Clean and return
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