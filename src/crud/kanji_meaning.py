"""
CRUD requests for the kanji meaning.
"""
from src.crud.base import CrudBase
from src.models import KanjiMeaning


class CrudKanjiMeaning(CrudBase[KanjiMeaning]):
    def __init__(self, Model: type[KanjiMeaning]):
        super().__init__(Model)
