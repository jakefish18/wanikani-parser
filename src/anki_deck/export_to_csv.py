import csv
import sys

sys.path.append("/home/jakefish/Documents/GitHub/wanikani-parser")

from src.crud import (
    CrudKanji,
    CrudKanjiMeaning,
    CrudKanjiReading,
    CrudWord,
    CrudWordContextSentence,
    CrudWordMeaning,
    CrudWordUsePattern,
)
from src.database import SessionLocal
from src.models import (
    Kanji,
    KanjiMeaning,
    KanjiReading,
    Word,
    WordContextSentence,
    WordMeaning,
    WordUsePattern,
)

crud_kanji = CrudKanji(Kanji)
crud_kanji_reading = CrudKanjiReading(KanjiReading)
crud_kanji_meaning = CrudKanjiMeaning(KanjiMeaning)
crud_word = CrudWord(Word)
crud_word_use_pattern = CrudWordUsePattern(WordUsePattern)
crud_word_context_sentence = CrudWordContextSentence(WordContextSentence)
crud_word_meaning = CrudWordMeaning(WordMeaning)


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
            kanji_radicals.append(kanji_radical.radical.meaning)
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
        kanji_primary_readings, kanji_reading_mnemonic, kanji_reading_mnemonic_note = (
            get_kanji_primary_readings(kanji)
        )
        kanji_primary_meaning, kanji_meaning_mnemonic, kanji_meaning_mnemonic_note = (
            get_kanji_primary_meaning(kanji)
        )
        kanji_rows.append(
            [
                kanji.level,
                kanji.symbol,
                kanji_radicals,
                kanji_primary_meaning,
                kanji_primary_readings,
                kanji_reading_mnemonic,
                kanji_reading_mnemonic_note,
                kanji_meaning_mnemonic,
                kanji_meaning_mnemonic_note,
            ]
        )

    db.close()
    return kanji_rows


def get_word_meanings(word: Word) -> str:
    """Get word meanings."""
    word_meanings = []

    for word_meaning in word.meanings:
        if word_meaning.is_primary:
            word_meanings.append(word_meaning.meaning)
        else:
            word_meanings.append(word_meaning.meaning + "(P)")

    return ", ".join(word_meanings)


def get_word_meaning_explanation(word: Word) -> str:
    """Get word meaning explanation."""
    return word.meanings[0].explanation


def get_word_context_sentences(word: Word) -> str:
    """Get word context sentences."""
    word_context_sentences = []

    for word_context_sentence in word.context_sentences:
        word_context_sentences.append(
            word_context_sentence.japanese + "\n" + word_context_sentence.english
        )

    return "\n\n".join(word_context_sentences)


def get_word_use_patterns(word: Word) -> str:
    """Get word use patterns."""
    word_use_patterns = []

    for word_use_pattern in word.use_patterns:
        word_use_patterns.append(
            f"{word_use_pattern.pattern}: {word_use_pattern.japanese}\n{word_use_pattern.english}"
        )

    return "\n\n".join(word_use_patterns)


def get_words_csv_rows(before_level: int) -> list[list[str]]:
    """
    Getting words from the database,
    which have lower or equal level than before_level.
    """
    db = SessionLocal()
    word_models: list[Word] = crud_word.get_words_before_level(db, before_level)
    word_rows = []

    for word in word_models:
        word_meanings = get_word_meanings(word)
        word_meaning_explanation = get_word_meaning_explanation(word)
        word_context_sentences = get_word_context_sentences(word)
        word_use_patterns = get_word_use_patterns(word)
        word_rows.append(
            [
                word.level,
                word.symbols,
                word.reading,
                word.reading_audio_filename,
                word.reading_explanation,
                word_meanings,
                word_meaning_explanation,
                word_context_sentences,
                word_use_patterns,
            ]
        )

    return word_rows


before_level = 10
deck_element = "words"
elements = []

match deck_element:
    case "kanji":
        elements = get_kanji_csv_rows(before_level=before_level)
    case "wk_radicals":
        pass
    case "words":
        elements = get_words_csv_rows(before_level=before_level)
    case _:
        raise ValueError(f"Unknown deck element: {deck_element}")

with open(
    "/home/jakefish/Documents/GitHub/wanikani-parser/src/output/deck.csv",
    "w",
    newline="\n",
) as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerows(elements)
