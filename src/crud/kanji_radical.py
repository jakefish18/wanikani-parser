"""
CRUD requests for the kanji radical.
"""
from src.crud.base import CrudBase
from src.models import KanjiRadical


class CrudKanjiRadical(CrudBase[KanjiRadical]):
    def __init__(self, Model: type[KanjiRadical]):
        super().__init__(Model)
