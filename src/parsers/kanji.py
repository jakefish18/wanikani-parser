import requests
import logging
logging.basicConfig(level=logging.INFO, filename="logs/kanji_parser.log", filemode="w")

from src.crud import CrudWKRadical, CrudKanjiReading, CrudKanjiMeaning, CrudKanjiRadical, CrudKanji
from src.parsers.base import BaseParser
from src.models import Kanji, KanjiMeaning, KanjiReading, KanjiRadical, WKRadical
from src.database import SessionLocal
from src.core import settings
from src.parsers.base import Mnemonic
from src.parsers import WKRadicalsParser


class Meaning:
    def __init__(self, meaning: str, is_primary: bool = False) -> None:
        self.meaning = meaning
        self.is_primary = is_primary


class Reading:
    def __init__(self, reading: str, reading_type: str, is_primary: bool = False) -> None:
        self.reading = reading
        self.type = reading_type
        self.is_primary = is_primary


class KanjiParser(BaseParser):
    def __init__(self):
        super().__init__()

        # The class name of the "a" tag which has link to the radical page.
        self.kanji_page_link_class = "subject-character subject-character--kanji subject-character--grid subject-character--unlocked"

        self.crud_kanji = CrudKanji(Kanji)
        self.crud_kanji_meaning = CrudKanjiMeaning(KanjiMeaning)
        self.crud_kanji_reading = CrudKanjiReading(KanjiReading)
        self.crud_kanji_radical = CrudKanjiRadical(KanjiRadical)
        self.crud_wk_radical = CrudWKRadical(WKRadical)

    def run(self) -> None:
        """
        Run the parser.
        """
        for difficulty_level in self.difficulty_levels:
            kanji_list_page_url = f"{settings.WANIKANI_BASE_URL}/kanji?difficulty={difficulty_level}"
            soup = self._get_page_soup(kanji_list_page_url)
            kanji_page_urls = self._get_element_links(soup, self.kanji_page_link_class)
            total_kanji_count = len(kanji_page_urls)

            for i, kanji_page_url in enumerate(kanji_page_urls):
                if not self._is_kanji_exists(kanji_page_url):
                    self._parse_kanji_page(kanji_page_url)
                else:
                    logging.warning(f"{kanji_page_url} already exists in the database.")
                logging.info(f"Processed {kanji_page_url} [{i + 1}/{total_kanji_count}]")

    def _is_kanji_exists(self, url: str) -> bool:
        """Checking if a kanji exists in the database by url."""
        with SessionLocal() as db:
            return self.crud_kanji.is_kanji_by_url(db, url)

    def _parse_kanji_page(self, kanji_page_url: str) -> Kanji:
        """
        Parsing the kanji info from page.

        Parameters:
            kanji_page_url: str - page of the kanji to parse

        Returns:
            WaniKaniRadical object
        """
        soup = self._get_page_soup(kanji_page_url)

        level = self._get_element_level(soup)
        symbol = soup.find("span", class_="page-header__icon page-header__icon--kanji").text.strip()

        radical_ids: list[int] = self._get_kanji_radicals(soup.find("section", {"id": "section-components"}))

        meanings: list[Meaning] = self._get_kanji_meanings(soup)
        meaning_mnemonic = self._get_mnemonic(soup, "subject-section subject-section--meaning")

        readings: list[Reading] = self._get_kanji_readings(soup)
        reading_mnemonic = self._get_mnemonic(soup, "subject-section subject-section--reading")

        # Highlighting radical meaning in mnemonic with the upper case.
        highlighted_radicals = self._get_highlighted_radicals(soup)
        highlighted_kanji = self._get_highlighted_kanji(soup)
        highlighted_readings = self._get_highlighted_readings(soup)

        for highlighted_word in highlighted_radicals + highlighted_kanji + highlighted_readings:
            meaning_mnemonic.mnemonic = self._highlight_text(meaning_mnemonic.mnemonic, highlighted_word)
            meaning_mnemonic.hint = self._highlight_text(meaning_mnemonic.hint, highlighted_word)

            reading_mnemonic.mnemonic = self._highlight_text(reading_mnemonic.mnemonic, highlighted_word)
            reading_mnemonic.hint = self._highlight_text(reading_mnemonic.hint, highlighted_word)

        with SessionLocal() as db:
            kanji = Kanji(
                level=level,
                symbol=symbol,
                url=kanji_page_url
            )
            kanji = self.crud_kanji.create(db, kanji)

            meanings_bulk_insert = self._create_meaning_bulk(kanji, meanings, meaning_mnemonic)
            self.crud_kanji_meaning.create_many(db, meanings_bulk_insert)

            readings_bulk_insert = self._create_reading_bulk(kanji, readings, reading_mnemonic)
            self.crud_kanji_reading.create_many(db, readings_bulk_insert)

            radicals_bulk_insert = self._create_radical_bulk(kanji, radical_ids)
            self.crud_kanji_radical.create_many(db, radicals_bulk_insert)

    def _get_kanji_radicals(self, soup) -> list[int]:
        """
        Getting kanji radicals.
        Returning kanji radicals ids.
        """
        kanji_radical_ids = []
        for kanji_radical_span in soup.find_all("span", class_="subject-character__meaning"):
            kanji_radical_meaning = kanji_radical_span.text

            with SessionLocal() as db:
                is_wk_radical = self.crud_wk_radical.is_radical_by_meaning(db, kanji_radical_meaning)

                if not is_wk_radical:
                    logging.critical(f"Radical {kanji_radical_meaning} doesn't exist in database")
                    logging.info(f"Running wk_radicals parser")
                    wk_radical_parser = WKRadicalsParser()
                    wk_radical_parser.run(is_download_image=True)

                wk_radical = self.crud_wk_radical.get_by_meaning(db, kanji_radical_meaning)
                kanji_radical_ids.append(wk_radical.id)

        return kanji_radical_ids

    def _get_kanji_meanings(self, soup) -> list[Meaning]:
        """
        Getting kanji meaning.
        One kanji can have multiple meanings: one primary meaning and some alternative meanings.
        For example, https://www.wanikani.com/kanji/%E4%B8%8A.

        Parameters:
            soup: BeautifulSoup - BeautifulSoup object.

        Returns:
            list[Meaning] - list of the meanings.
        """
        meanings = []

        for div_meaning in soup.find_all("div", class_="subject-section__meanings"):
            meaning_type = div_meaning.find("h2", class_="subject-section__meanings-title").text
            meaning_text = div_meaning.find("p", class_="subject-section__meanings-items").text

            if meaning_type == "Primary":
                meanings.append(Meaning(meaning=meaning_text, is_primary=True))
            else:
                meanings.extend([Meaning(meaning=meaning) for meaning in meaning_text.split(", ")])

        return meanings

    def _get_kanji_readings(self, soup) -> list[Reading]:
        """
        Getting kanji readings.
        One kanji can have multiple readings of three types: on-yomi, kun-yomi, nanori.
        There is one primary reading and some alternative readings.
        For example, https://www.wanikani.com/kanji/%E5%A7%94.

        Parameters:
            soup: BeautifulSoup - BeautifulSoup object.

        Returns:
            list[Reading] - list of the readings.
        """
        readings = []

        for reading_type_div in soup.find_all("div", class_="subject-readings__reading"):
            reading_type = reading_type_div.find("h3", class_="subject-readings__reading-title").text.strip()
            reading_text = reading_type_div.find("p", class_="subject-readings__reading-items").text.strip()
            is_primary = "subject-readings__reading--primary" in reading_type_div.get("class")

            if reading_text == "None":
                continue

            for reading in reading_text.split(", "):
                # Reading type is primary reading type if it has specific class.
                readings.append(Reading(reading=reading.strip(), reading_type=reading_type, is_primary=is_primary))

        return readings

    def _create_meaning_bulk(self, kanji: Kanji, meanings: list[Meaning], meaning_mnemonic: Mnemonic) -> list[KanjiMeaning]:
        meaning_bulk = []

        for meaning in meanings:
            # Meaning doesn't have mnemonic if it's not primary.
            if meaning.is_primary:
                meaning_bulk.append(
                    KanjiMeaning(
                        kanji_id=kanji.id,
                        meaning=meaning.meaning,
                        is_primary=meaning.is_primary,
                        mnemonic=meaning_mnemonic.mnemonic,
                        mnemonic_hint=meaning_mnemonic.hint
                    )
                )
            else:
                meaning_bulk.append(
                    KanjiMeaning(
                        kanji_id=kanji.id,
                        meaning=meaning.meaning,
                        is_primary=meaning.is_primary,
                    )
                )

        return meaning_bulk

    def _create_reading_bulk(self, kanji: Kanji, readings: list[Reading], reading_mnemonic: Mnemonic) -> list[KanjiReading]:
        reading_bulk = []

        for reading in readings:
            # Reading doesn't have mnemonic if it's not primary.
            if reading.is_primary:
                reading_bulk.append(
                    KanjiReading(
                        kanji_id=kanji.id,
                        reading=reading.reading,
                        is_primary=reading.is_primary,
                        mnemonic=reading_mnemonic.mnemonic,
                        mnemonic_hint=reading_mnemonic.hint
                    )
                )
            else:
                reading_bulk.append(
                    KanjiReading(
                        kanji_id=kanji.id,
                        reading=reading.reading,
                        is_primary=reading.is_primary,
                    )
                )

        return reading_bulk
    def _create_radical_bulk(self, kanji: Kanji, radical_ids: list[int]) -> list[KanjiRadical]:
        radical_bulk = []

        for radical_id in radical_ids:
            radical_bulk.append(KanjiRadical(
                kanji_id=kanji.id,
                wk_radical_id=radical_id
            ))

        return radical_bulk