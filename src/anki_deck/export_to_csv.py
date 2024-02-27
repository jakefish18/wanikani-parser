import csv

from src.database import SessionLocal
from src.models import Kanji, KanjiReading, KanjiMeaning
from src.crud import CrudKanji, CrudKanjiReading, CrudKanjiMeaning
crud_kanji = CrudKanji(Kanji)
crud_kanji_reading = CrudKanjiReading(KanjiReading)
crud_kanji_meaning = CrudKanjiMeaning(KanjiMeaning)


def get_kanji_primary_readings(kanji: Kanji) -> [str, str, str]:
    """
    Getting the primary reading of a kanji.
    Function returns the joined with commas string of readings.

    Returns:
        str: The primary readings of a kanji splited with the comma.
        str: The mnemonic for primary reading.
        str: The mnemonic note.
    """
    primary_readings = []
    mnemonic = ""
    mnemonic_note = ""

    with SessionLocal() as db:
        for primary_reading in crud_kanji_reading.get_primary_readings(db, kanji):
            reading_type = ""

            match primary_reading.type:
                case "On’yomi":
                    reading_type = "O"
                case "Kun’yomi":
                    reading_type = "K"
                case "Nanori":
                    reading_type = "N"
                case _:
                    raise ValueError(f"Unknown reading type {primary_reading.type}")

            mnemonic = primary_reading.mnemonic
            mnemonic_note = primary_reading.mnemonic_hint
            primary_readings.append(f"{primary_reading.reading}({reading_type})")

    return ", ".join(primary_readings), mnemonic, mnemonic_note


def get_kanji_primary_meaning(kanji: Kanji) -> [str, str, str]:
    """
    Getting the primary meaning of a kanji.

    Returns:
        str: The primary meaning of a kanji.
        str: The mnemonic for primary meaning.
        str: The mnemonic note.
    """
    primary_meaning = ""
    mnemonic = ""
    mnemonic_note = ""

    with SessionLocal() as db:
        primary_meaning_model = crud_kanji_meaning.get_primary_meaning(db, kanji)
        primary_meaning = primary_meaning_model.meaning
        mnemonic = primary_meaning_model.mnemonic
        mnemonic_note = primary_meaning_model.mnemonic_hint

    return primary_meaning, mnemonic, mnemonic_note


def get_kanji_radicals(kanji: Kanji) -> str:
    """
    Getting the kanji radicals.

    Returns:
        str: The radicals joined with + sign.
    """
    kanji_radicals = []

    for kanji_radical in kanji.radicals:
        # Some radicals don't plain symbol.
        if kanji_radical.radical.symbol:
            kanji_radicals.append(kanji_radical.radical.symbol)
        else:
            kanji_radicals.append(kanji_radical.radical.meaning
                                  )
    return " + ".join(kanji_radicals)

def get_kanji_by_level(before_level: int) -> list[Kanji]:
    """
    Getting kanji from the database,
    which have lower or equal level than before_level.
    """
    with SessionLocal() as db:
        return crud_kanji.get_by_level(db, before_level)

def get_kanji_csv_rows(before_level: int) -> list[list[str]]:
    """
    Getting kanji from the database,
    which have lower or equal level than before_level.
    """
    db = SessionLocal()
    kanji_models = crud_kanji.get_by_level(db, before_level)
    kanji_rows = []

    for kanji in kanji_models:
        kanji_radicals = get_kanji_radicals(kanji)
        kanji_primary_readings, kanji_reading_mnemonic, kanji_reading_mnemonic_note = get_kanji_primary_readings(kanji)
        kanji_primary_meaning, kanji_meaning_mnemonic, kanji_meaning_mnemonic_note = get_kanji_primary_meaning(kanji)
        kanji_rows.append([
            kanji.level,
            kanji.symbol,
            kanji_radicals,
            kanji_primary_meaning,
            kanji_primary_readings,
            kanji_reading_mnemonic,
            kanji_reading_mnemonic_note,
            kanji_meaning_mnemonic,
            kanji_meaning_mnemonic_note
        ])

        if kanji.symbol == "出":
            print(kanji_rows[-1])

    db.close()
    return kanji_rows


before_level = 10
deck_element = "kanji"
elements = []

match deck_element:
    case "kanji":
        elements = get_kanji_csv_rows(before_level=before_level)
    case "wk_radicals":
        pass
    case "words":
        pass
    case _:
        raise ValueError(f"Unknown deck element: {deck_element}")

with open("/home/jakefish/Documents/GitHub/wanikani-parser/src/output/deck.csv", "w", newline="\n") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerows(elements)
