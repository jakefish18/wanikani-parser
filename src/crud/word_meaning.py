"""
CRUD requests for the word meanings.
"""
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import WordMeaning


class CrudWordMeaning(CrudBase[WordMeaning]):
    def __init__(self, Model: type[WordMeaning]):
        super().__init__(Model)
