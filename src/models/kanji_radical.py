"""A kanji radical SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class KanjiRadical(Base):
    __tablename__ = "kanji_radicals"

    id = Column(Integer, primary_key=True, index=True)
    kanji_id = Column(Integer, ForeignKey("kanji.id", ondelete="CASCADE"))
    wk_radical_id = Column(Integer, ForeignKey("wk_radicals.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    kanji = relationship("Kanji", back_populates="radicals", uselist=False)
    radical = relationship("WKRadical", back_populates="kanji", uselist=False)