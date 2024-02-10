"""
CRUD requests for the kanji reading.
"""
from src.crud.base import CrudBase
from src.models import KanjiReading


class CrudKanjiReading(CrudBase[KanjiReading]):
    def __init__(self, Model: type[KanjiReading]):
        super().__init__(Model)
