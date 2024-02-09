"""
CRUD requests for the words.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import Word


class CrudWord(CrudBase[Word]):
    def __init__(self, Model: type[Word]):
        super().__init__(Model)
