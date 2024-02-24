"""
CRUD requests for the words.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import Word


class CrudWord(CrudBase[Word]):
    def __init__(self, Model: type[Word]):
        super().__init__(Model)

    def is_word_by_url(self, db: Session, url: str) -> bool:
        """Checking if a word exists in the database."""
        return self.get_word_by_url(db, url) != None

    def get_word_by_url(self, db: Session, url: str) -> Word:
        """Get a word by its url."""
        return db.query(Word).filter(Word.url == url).first()