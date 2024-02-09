"""
CRUD requests for the kanji.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import Kanji


class CrudKanji(CrudBase[Kanji]):
    def __init__(self, Model: type[Kanji]):
        super().__init__(Model)
