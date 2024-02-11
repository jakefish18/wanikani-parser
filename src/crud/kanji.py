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
        return self.get_kanji_by_url(db, url) != None

    def get_kanji_by_url(self, db: Session, url: str) -> Kanji:
        """Geting a kanji by its url."""
        return db.query(Kanji).filter(Kanji.url == url).first()
