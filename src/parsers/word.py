import logging

from src.crud import CrudWord, CrudWordContextSentence, CrudWordMeaning, CrudWordUsePatterns
from src.parsers.base import BaseParser, Meaning, Mnemonic
from src.models import Word, WordMeaning, WordUsePattern, WordContextSentence
from src.database import SessionLocal
from src.core import settings


class AudioType:
    WEBM = "webm"
    MPEG = "mpeg"


class Sentence:
    """
    Class representing a sentence.
    There are two attributes: japanese and english texts.
    """
    def __init__(self, japanese: str, english: str) -> None:
        self.japanese = japanese
        self.english = english


class UsePatternExample(Sentence):
    def __init__(self, japanese: str, english: str) -> None:
        super().__init__(japanese, english)


class UsePattern:
    def __init__(self, pattern: str, example: UsePatternExample) -> None:
        self.pattern = pattern
        self.example = example


class ContextSentence(Sentence):
    def __init__(self, japanese: str, english: str) -> None:
        super().__init__(japanese, english)


class WordParser(BaseParser):
    def __init__(self, is_download_audio: bool = True) -> None:
        super().__init__()

        self.is_download_audio = is_download_audio

        # The class name of the "a" tag which has link to the wrod page.
        self.word_page_link_class = ("subject-character subject-character--vocabulary "
                                     "subject-character--grid subject-character--unlocked")

        self.crud_word = CrudWord(Word)
        self.crud_word_context_sentence = CrudWordContextSentence(WordContextSentence)
        self.crud_word_use_pattern = CrudWordUsePatterns(WordUsePattern)
        self.crud_word_meaning = CrudWordMeaning(WordMeaning)

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
        reading_audio_name = ""

        if self.is_download_audio:
            reading_audio_name = self._download_reading_audio(soup, symbols, AudioType.MPEG)

        context_sentences: list[WordContextSentence] = self._get_context_sentences(soup)
        use_patterns: list[WordUsePattern] = self._get_use_patterns(soup)

        # Insert all data into the database.
        with SessionLocal() as db:
            # Insert word.
            word = self.crud_word.create(db, Word(
                url=word_page_url,
                level=level,
                symbols=symbols,
                reading=reading,
                reading_audio_filename=reading_audio_name
            ))

            # Insert context sentences.
            for context_sentence in context_sentences:
                context_sentence.word_id = word.id

            self.crud_word_context_sentence.create_many(db, context_sentences)

            # Insert meanings.
            meaning_bulk = []
            for meaning in meanings:
                meaning_bulk.append(WordMeaning(
                    word_id=word.id,
                    meaning=meaning.meaning,
                    is_primary=meaning.is_primary,
                    explanation=meaning_explanation.mnemonic
                ))

            self.crud_word_meaning.create_many(db, meaning_bulk)

            # Insert use patterns.
            for use_pattern in use_patterns:
                use_pattern.word_id = word.id

            self.crud_word_use_pattern.create_many(db, use_patterns)


    def _get_reading(self, soup):
        """
        Get word reading from the soup.

        Parameters:
            soup: BeautifulSoup object
        """
        return soup.find("div", class_="reading-with-audio__reading").text.strip()

    def _download_reading_audio(self, soup, symbols: str, prefered_file_type: str) -> str | None:
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

        if not audio_block:
            return None

        webm_audio_element, mpeg_audio_element = audio_block.find_all("source")
        downloading_audio_url = ""

        match prefered_file_type:
            case AudioType.WEBM:
                downloading_audio_url = webm_audio_element.get("src")
            case AudioType.MPEG:
                downloading_audio_url = mpeg_audio_element.get("src")
            case _:
                raise ValueError(f"There is no type {prefered_file_type} for audio.")

        file_name = f"audio_{symbols}.{prefered_file_type}"
        file_path = f"output/audio/{file_name}"
        self._download_file(file_path, downloading_audio_url)

        return file_name

    def _get_use_patterns(self, soup) -> list[WordUsePattern]:
        """
        Get a list of the use patterns for the word.

        Parameters:
            soup: BeautifulSoup object.

        Returns:
            use_patterns: list[WordUsePattern] - list of use patterns.
        """
        use_patterns: list[WordUsePattern] = []

        use_pattern_list = soup.find_all("a", class_="subject-collocations__pattern-name") or []
        example_lists = soup.find_all("li", class_="subject-collocations__pattern-collocation") or []

        for use_pattern, example_list in zip(use_pattern_list, example_lists):
            for example_block in example_list.find_all("div", class_="context-sentences"):
                japanese_sentence, english_sentence = example_block.find_all("p")
                japanese_sentence, english_sentence = japanese_sentence.text.strip(), english_sentence.text.strip()

                use_patterns.append(WordUsePattern(
                    pattern=use_pattern.text.strip(),
                    japanese=japanese_sentence,
                    english=english_sentence
                ))

        return use_patterns


    def _get_context_sentences(self, soup) -> list[ContextSentence]:
        """
        Get a list of contextual sentences for the word.

        Args:
            soup: BeautifulSoup object

        Returns:
            context_sentences: list[ContextSentence] - list of contextual sentences.
        """
        context_sentences = []

        for sentence_block in soup.find_all("div", class_="subject-section__text subject-section__text--grouped"):
            japanese_sentence, english_sentence = sentence_block.find_all("p")
            japanese_sentence, english_sentence = japanese_sentence.text.strip(), english_sentence.text.strip()

            context_sentences.append(
                WordContextSentence(
                    japanese=japanese_sentence,
                    english=english_sentence
                )
            )

        return context_sentences


if __name__ == "__main__":
    word_parser = WordParser()
    word_parser.run()
