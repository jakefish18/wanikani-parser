import asyncio
import sys
import time

sys.path.append("..")

# Logging.
import logging

logging.basicConfig(level=logging.INFO, filename="logs/logs.log", filemode="w")

import src.models

# Database initialization.
from src.database import Base, engine

Base.metadata.create_all(engine)

from src.parsers import KanjiParser, WKRadicalsParser, WordParser

word_parser = WordParser(is_download_audio=True)
radicals_parser = WKRadicalsParser()
kanji_parser = KanjiParser()

loop = asyncio.get_event_loop()

while True:
    try:
        loop.run_until_complete(word_parser.run())
        loop.run_until_complete(radicals_parser.run())
        loop.run_until_complete(kanji_parser.run())
    
    except Exception as e:
        logging.warning("Error while parsing. Relaunching after 10 seconds.")
        logging.warning(e)
        
        for i in range(10, 0, -1):
            logging.info(f"{i} second before relaunch...")
            time.sleep(1)