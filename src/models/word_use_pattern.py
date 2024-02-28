"""A word use pattern SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database import Base


class WordUsePattern(Base):
    __tablename__ = "word_use_pattern"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("word.id", ondelete="CASCADE"))
    pattern = Column(String)
    example_japanese = Column(String)
    example_english = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    word = relationship("Word", back_populates="use_patterns", uselist=False)
