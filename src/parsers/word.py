import requests
import logging
logging.basicConfig(level=logging.INFO, filename="logs/kanji_parser.log", filemode="w")

from src.crud import CrudWKRadical, CrudKanjiReading, CrudKanjiMeaning, CrudKanjiRadical, CrudKanji, CrudWord
from src.parsers.base import BaseParser, Meaning
from src.models import Kanji, KanjiMeaning, KanjiReading, KanjiRadical, WKRadical, Word
from src.database import SessionLocal
from src.core import settings
from src.parsers import WKRadicalsParser, KanjiParser


class WordParser(BaseParser):
    def __init__(self):
        super().__init__()

        # The class name of the "a" tag which has link to the wrod page.
        self.word_page_link_class = ("subject-character subject-character--vocabulary "
                                     "subject-character--grid subject-character--unlocked")

        self.crud_kanji = CrudKanji(Kanji)
        self.crud_kanji_meaning = CrudKanjiMeaning(KanjiMeaning)
        self.crud_kanji_reading = CrudKanjiReading(KanjiReading)
        self.crud_kanji_radical = CrudKanjiRadical(KanjiRadical)
        self.crud_wk_radical = CrudWKRadical(WKRadical)
        self.crud_word = CrudWord(Word)

    def run(self) -> None:
        """
        Run the parser.
        """
        for difficulty_level in self.difficulty_levels:
            word_list_page_url = f"{settings.WANIKANI_BASE_URL}/vocabulary?difficulty={difficulty_level}"
            soup = self._get_page_soup(word_list_page_url)
            word_page_urls = self._get_element_links(soup, self.word_page_link_class)
            total_word_count = len(word_page_urls)

            for i, word_page_url in enumerate(word_page_urls):
                if not self._is_word_exists(word_page_url):
                    self._parse_word_page(word_page_url)
                else:
                    logging.warning(f"{word_page_url} already exists in the database.")
                logging.info(f"Processed {word_page_url} [{i + 1}/{total_word_count}]")

    def _is_word_exists(self, url: str) -> bool:
        """Checking if a word exists in the database by url."""
        with SessionLocal() as db:
            return self.crud_word.is_word_by_url(db, url)

    def _parse_word_page(self, word_page_url: str) -> Word:
        """
        Parsing the word info from the page.

        Parameters:
            word_page_url: str - page of the word to parse

        Returns:
            Word object
        """
        soup = self._get_page_soup(word_page_url)

        level = self._get_element_level(soup)
        word_symbols = soup.find("span", class_="page-header__icon page-header__icon--vocabulary").text.strip()
        word_meanings: list[Meaning] = self._get_element_meanings(soup)

    def _get_meaning_explanation(self, soup):
        """"""
        pass

    def _get_reading(self, soup):
        """
        """
        pass

    def _get_reading_explanation(self, soup):
        """
        """
        pass

    def _get_reading_audio(self, soup):
        """
        """
        pass

    def _get_context_sentences(self, soup):
        """"""
        pass


if __name__ == "__main__":
    word_parser = WordParser()
    word_parser.run()
