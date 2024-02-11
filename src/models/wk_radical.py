"""A WaniKani radical SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class WKRadical(Base):
    __tablename__ = "wk_radicals"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    symbol = Column(String)
    meaning = Column(String)
    mnemonic = Column(String)
    image_filename = Column(String, nullable=True)
    is_symbol_image = Column(Boolean, default=False)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    kanji = relationship("KanjiRadical", back_populates="radical")
