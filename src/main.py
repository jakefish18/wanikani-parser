# Database initialization.
from src.database import engine, Base
import src.models
Base.metadata.create_all(engine)


from src.parsers import KanjiParser

kanji_parser = KanjiParser()
kanji_parser.run()
