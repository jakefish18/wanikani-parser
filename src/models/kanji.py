"""A kanji SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Kanji(Base):
    __tablename__ = "kanji"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    radicals = relationship("KanjiRadical", back_populates="kanji")
    readings = relationship("KanjiReading", back_populates="kanji")
    meanings = relationship("KanjiMeaning", back_populates="kanji")