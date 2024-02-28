"""
CRUD requests for the word context sentences.
"""
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import WordContextSentence


class CrudWordContextSentence(CrudBase[WordContextSentence]):
    def __init__(self, Model: type[WordContextSentence]):
        super().__init__(Model)
