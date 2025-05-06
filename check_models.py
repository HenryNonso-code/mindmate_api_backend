import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file locally
load_dotenv()

# Prefer GOOGLE_API_KEY (Render) or fallback to GEMINI_API_KEY (.env)
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Ensure an API key was found
if not api_key:
    raise ValueError("❌ No API key found. Set GOOGLE_API_KEY in Render or GEMINI_API_KEY in .env.")

# Configure Gemini
genai.configure(api_key=api_key)

# List and print available models
try:
    models = genai.list_models()
    for model in models:
        print("✅", model.name)
except Exception as e:
    print("❌ Error listing models:", e)