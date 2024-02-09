"""A kanji radical SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.database import Base


class KanjiRadical(Base):
    __tablename__ = "kanji_radicals"

    id = Column(Integer, primary_key=True, index=True)
    kanji = Column(String)
    radical = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
