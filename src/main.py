# Database initialization.
from src.database import engine, Base
import src.models
Base.metadata.create_all(engine)

from src.parsers import KanjiParser, WKRadicalsParser

wk_radical_parser = WKRadicalsParser()
wk_radical_parser.run(is_download_image=True)

kanji_parser = KanjiParser()
kanji_parser.run()