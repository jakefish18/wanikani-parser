"""
CRUD requests for the WaniKani radicals.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import WKRadical


class CrudWKRadical(CrudBase[WKRadical]):
    def __init__(self, Model: type[WKRadical]):
        super().__init__(Model)

    def is_radical_by_symbol(self, db: Session, symbol: str) -> bool:
        """Checking if there is radical with the given symbol."""
        return self.get_by_symbol(db, symbol) != None

    def is_radical_by_meaning(self, db: Session, meaning: str) -> bool:
        """Checking if there is radical with the given meaning."""
        return self.get_by_meaning(db, meaning) != None

    def is_radical_by_url(self, db: Session, url: str) -> bool:
        """Checking if there is radical with the given url."""
        return self.get_by_url(db, url) != None

    def get_by_symbol(self, db: Session, symbol: str) -> WKRadical:
        """Getting the wanikani radical object by its symbol."""
        return db.query(WKRadical).filter(WKRadical.symbol == symbol).first()

    def get_by_meaning(self, db: Session, meaning: str) -> WKRadical:
        """Getting the wanikani radcial object by its meaning."""
        return db.query(WKRadical).filter(WKRadical.meaning == meaning).first()

    def get_by_url(self, db: Session, url: str) -> WKRadical:
        """Getting the wanikani radcial object by its url."""
        return db.query(WKRadical).filter(WKRadical.url == url).first()