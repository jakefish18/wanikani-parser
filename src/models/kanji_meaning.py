"""A kanji meaning SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class KanjiMeaning(Base):
    __tablename__ = "kanji_meanings"

    id = Column(Integer, primary_key=True, index=True)
    kanji_id = Column(Integer, ForeignKey("kanji.id", ondelete="CASCADE"))
    meaning = Column(String)
    is_primary = Column(Boolean, default=False)
    mnemonic = Column(String, nullable=True)
    mnemonic_hint = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    kanji = relationship("Kanji", back_populates="meanings", uselist=False)
