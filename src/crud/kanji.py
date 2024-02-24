"""
CRUD requests for the kanji.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import Kanji


class CrudKanji(CrudBase[Kanji]):
    def __init__(self, Model: type[Kanji]):
        super().__init__(Model)

    def is_kanji_by_url(self, db: Session, url: str) -> bool:
        """Checking if a kanji exists in the database."""
        return self.get_by_url(db, url) != None

    def get_by_url(self, db: Session, url: str) -> Kanji:
        """Getting a kanji by its url."""
        return db.query(Kanji).filter(Kanji.url == url).first()

    def get_by_level(self, db: Session, before_level: int) -> list[Kanji]:
        """Getting the kanji which have level lower than before_level."""
        return db.query(Kanji).filter(Kanji.level <= before_level).all()

