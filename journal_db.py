from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    id = Column(Integer, primary_key=True, index=True)
    mood = Column(String)
    affirmation = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine("sqlite:///./journal.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)