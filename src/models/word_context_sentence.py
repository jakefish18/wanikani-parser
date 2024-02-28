"""A word context sentence SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database import Base


class WordContextSentence(Base):
    __tablename__ = "word_context_sentence"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("word.id", ondelete="CASCADE"))
    japanese = Column(String)
    english = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    word = relationship("Word", back_populates="context_sentences", uselist=False)
