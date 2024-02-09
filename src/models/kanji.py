"""A kanji SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.database import Base


class Kanji(Base):
    __tablename__ = "kanji"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    meaning = Column(String)
    mnemonic = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

