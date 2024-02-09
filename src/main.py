# Database initialization.
from src.database import engine, Base
import src.models
Base.metadata.create_all(engine)


from src.parsers import WKRadicalsParser

wk_radical_parser = WKRadicalsParser()
wk_radical_parser.run()

