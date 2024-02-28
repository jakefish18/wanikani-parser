"""A word meaning SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class WordMeaning(Base):
    __tablename__ = "word_meaning"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("word.id", ondelete="CASCADE"))
    meaning = Column(String)
    is_primary = Column(Boolean)
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    word = relationship("Word", back_populates="meanings", uselist=False)
