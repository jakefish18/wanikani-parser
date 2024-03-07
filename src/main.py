import asyncio
import sys

sys.path.append("..")

# Logging.
import logging

logging.basicConfig(level=logging.INFO, filename="logs/logs.log", filemode="w")

import src.models

# Database initialization.
from src.database import Base, engine

Base.metadata.create_all(engine)

from src.parsers import KanjiParser, WKRadicalsParser, WordParser

word_parser = WordParser(is_download_audio=False)

loop = asyncio.get_event_loop()
loop.run_until_complete(word_parser.run())
