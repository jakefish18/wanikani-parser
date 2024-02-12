"""
CRUD requests for the kanji meaning.
"""
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import KanjiMeaning, Kanji


class CrudKanjiMeaning(CrudBase[KanjiMeaning]):
    def __init__(self, Model: type[KanjiMeaning]):
        super().__init__(Model)

    def get_primary_meaning(self, db: Session, kanji: Kanji) -> KanjiMeaning | None:
        """Getting the primary meaning of the kanji."""
        return db.query(KanjiMeaning).filter(
            and_(
                KanjiMeaning.kanji_id == kanji.id,
                KanjiMeaning.is_primary
            )
        ).first()