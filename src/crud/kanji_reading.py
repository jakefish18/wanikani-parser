"""
CRUD requests for the kanji reading.
"""
from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import Type

from src.crud.base import CrudBase
from src.models import KanjiReading, Kanji


class CrudKanjiReading(CrudBase[KanjiReading]):
    def __init__(self, Model: type[KanjiReading]):
        super().__init__(Model)

    def get_primary_readings(self, db: Session, kanji: Kanji) -> list[Type[KanjiReading]]:
        """Getting the primary readings of the kanji."""
        return db.query(KanjiReading).filter(
            and_(
                KanjiReading.is_primary,
                KanjiReading.kanji_id == kanji.id)
        ).all()