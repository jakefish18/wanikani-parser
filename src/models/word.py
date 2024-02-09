"""A japanese vocabulary word SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    meaning = Column(String)
    mnemonic = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

