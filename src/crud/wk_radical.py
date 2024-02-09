"""
CRUD requests for the WaniKani radicals.
"""
from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import WKRadical


class CrudWKRadical(CrudBase[WKRadical]):
    def __init__(self, Model: type[WKRadical]):
        super().__init__(Model)
