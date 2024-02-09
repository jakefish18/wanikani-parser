"""A WaniKani radical SQLAlchemy model."""
import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.database import Base


class WKRadical(Base):
    __tablename__ = "wk_radicals"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    symbol = Column(String)
    meaning = Column(String)
    mnemonic = Column(String)
    image_filename = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

