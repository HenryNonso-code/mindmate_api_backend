from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from gemini_agent import generate_affirmation
from journal_db import SessionLocal, JournalEntry
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MindMate AI")

@app.get("/")
def read_root():
    return {"message": "Welcome to MindMate AI backend!"}

@app.get("/affirmation")
def get_affirmation(mood: str = Query(..., description="Your current mood")):
    try:
        logger.info(f"Received mood: {mood}")

        affirmation = generate_affirmation(mood)
        logger.info(f"Generated affirmation: {affirmation}")

        db: Session = SessionLocal()
        entry = JournalEntry(mood=mood, affirmation=affirmation)
        db.add(entry)
        db.commit()
        db.close()

        return {
            "mood": mood,
            "affirmation": affirmation
        }
    except Exception as e:
        logger.error(f"Error in /affirmation: {str(e)}")
        return JSONResponse(content={"error": "Internal Server Error", "details": str(e)}, status_code=500)

@app.get("/journal")
def read_journal():
    try:
        db: Session = SessionLocal()
        entries = db.query(JournalEntry).order_by(JournalEntry.timestamp.desc()).all()
        db.close()

        data = [
            {
                "id": entry.id,
                "mood": entry.mood,
                "affirmation": entry.affirmation,
                "timestamp": entry.timestamp.isoformat()
            }
            for entry in entries
        ]

        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error in /journal: {str(e)}")
        return JSONResponse(content={"error": "Internal Server Error", "details": str(e)}, status_code=500)
