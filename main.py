from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from gemini_agent import generate_affirmation
from journal_db import SessionLocal, JournalEntry

app = FastAPI(title="MindMate AI")

@app.get("/")
def read_root():
    return {"message": "Welcome to MindMate AI backend!"}

@app.get("/affirmation")
def get_affirmation(mood: str = Query(..., description="Your current mood")):
    # Generate affirmation
    affirmation = generate_affirmation(mood)

    # Save to journal
    db: Session = SessionLocal()
    entry = JournalEntry(mood=mood, affirmation=affirmation)
    db.add(entry)
    db.commit()
    db.close()

    return {
        "mood": mood,
        "affirmation": affirmation
    }

@app.get("/journal")
def read_journal():
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
