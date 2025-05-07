import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.oauth2 import service_account

# ----------------------
# Load environment variables from .env
# ----------------------
load_dotenv()

# ----------------------
# Get path to service account JSON
# ----------------------
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# DEBUG: Print what path we are testing
print("Credential path from .env:", credentials_path)
print("File exists:", os.path.exists(credentials_path))

# Validate that path exists
if not credentials_path or not os.path.exists(credentials_path):
    raise ValueError(f"❌ Invalid GOOGLE_APPLICATION_CREDENTIALS: {credentials_path}")

# ----------------------
# Load credentials and configure Gemini
# ----------------------
credentials = service_account.Credentials.from_service_account_file(credentials_path)
genai.configure(credentials=credentials)

# ----------------------
# Generate mood-based affirmation
# ----------------------
def generate_affirmation(mood: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
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
