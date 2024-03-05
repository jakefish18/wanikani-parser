"""
CRUD requests for the word use patterns.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import WordUsePattern


class CrudWordUsePattern(CrudBase[WordUsePattern]):
    def __init__(self, Model: type[WordUsePattern]):
        super().__init__(Model)