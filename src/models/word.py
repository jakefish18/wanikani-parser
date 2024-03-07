"""A japanese vocabulary word SQLAlchemy model."""

import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    url = Column(String, unique=True, index=True)
    symbols = Column(String)
    reading = Column(String)
    reading_explanation = Column(String)
    reading_audio_filename = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    context_sentences = relationship("WordContextSentence", back_populates="word")
    meanings = relationship("WordMeaning", back_populates="word")
    use_patterns = relationship("WordUsePattern", back_populates="word")
