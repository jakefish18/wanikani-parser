import sys
sys.path.append('..')

# Logging.
import logging
logging.basicConfig(level=logging.INFO, filename="logs/logs.log", filemode="w")

# Database initialization.
from src.database import engine, Base
import src.models
Base.metadata.create_all(engine)

from src.parsers import KanjiParser, WKRadicalsParser, WordParser


word_parser = WordParser()
word_parser.run()

