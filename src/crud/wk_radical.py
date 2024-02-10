"""
CRUD requests for the WaniKani radicals.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import WKRadical


class CrudWKRadical(CrudBase[WKRadical]):
    def __init__(self, Model: type[WKRadical]):
        super().__init__(Model)

    def get_by_symbol(self, db: Session, symbol: str) -> WKRadical:
        """Getting the wanikani radical object by its symbol."""
        return db.query(WKRadical).filter(WKRadical.symbol == symbol).first()