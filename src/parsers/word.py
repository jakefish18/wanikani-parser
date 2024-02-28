import requests
import logging
logging.basicConfig(level=logging.INFO, filename="logs/kanji_parser.log", filemode="w")

from src.crud import CrudWKRadical, CrudKanjiReading, CrudKanjiMeaning, CrudKanjiRadical, CrudKanji, CrudWord
from src.parsers.base import BaseParser, Meaning, Mnemonic
from src.models import Kanji, KanjiMeaning, KanjiReading, KanjiRadical, WKRadical, Word
from src.database import SessionLocal
from src.core import settings


class AudioType:
    WEBM = "webm"
    MPEG = "mpeg"


class WordParser(BaseParser):
    def __init__(self, is_download_audio: bool = True) -> None:
        super().__init__()

        self.is_download_audio = is_download_audio

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
        symbols = soup.find("span", class_="page-header__icon page-header__icon--vocabulary").text.strip()

        meanings: list[Meaning] = self._get_element_meanings(soup)
        meaning_explanation: Mnemonic = self._get_mnemonic(soup, "subject-section--meaning")

        reading = self._get_reading(soup)
        reading_explanation: Mnemonic = self._get_mnemonic(soup, "subject-section--reading")
        reading_audio_file_path = ""

        if self.is_download_audio:
            reading_audio_file_path = self._download_reading_audio(soup, AudioType.MPEG, symbols)

    def _get_reading(self, soup):
        """
        Get word reading from the soup.

        Parameters:
            soup: BeautifulSoup object
        """
        return soup.find("div", class_="reading-with-audio__reading").text.strip()

    def _download_reading_audio(self, soup, prefered_file_type: AudioType, meaning: str) -> str:
        """
        Get reading audio.
        There are two audio for the vocabulary word:
        one with female voice and one with male voice.
        Because I don't see the reason to parse both voices,
        I will parse only female voice.

        Parameters:
            soup: BeautifulSoup object

        Returns:
            audio_file_name: str - name of the audio file.
        """
        audio_block = soup.find("audio", class_="reading-with-audio__audio")
        webm_audio_element, mpeg_audio_element = audio_block.find_all("source")
        downloading_audio_url = ""

        match prefered_file_type:
            case AudioType.WEBM:
                downloading_audio_url = webm_audio_element.get("src")
            case AudioType.MPEG:
                downloading_audio_url = mpeg_audio_element.get("src")
            case _:
                raise ValueError(f"There is no type {prefered_file_type} for audio.")

        file_path = f"output/audio/audio_{meaning}.{prefered_file_type}"
        self._download_file(file_path, downloading_audio_url)

        return file_path

    def _get_context_sentences(self, soup):
        """"""
        pass


if __name__ == "__main__":
    word_parser = WordParser()
    word_parser.run()
