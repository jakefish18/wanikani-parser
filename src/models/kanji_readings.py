"""Kanji reading QLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class KanjiReading(Base):
    __tablename__ = "kanji_readings"

    id = Column(Integer, primary_key=True, index=True)
    kanji_id = Column(Integer, ForeignKey("kanji.id", ondelete="CASCADE"))
    reading = Column(String)
    type = Column(String)
    mnemonic = Column(String, nullable=True)
    mnemonic_hint = Column(String, nullable=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    kanji = relationship("Kanji", back_populates="readings")
