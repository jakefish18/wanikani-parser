import aiohttp
import requests
from bs4 import BeautifulSoup

from src.core import settings


class Mnemonic:
    def __init__(self, mnemonic: str, hint: str) -> None:
        self.mnemonic = mnemonic
        self.hint = hint


class Meaning:
    def __init__(self, meaning: str, is_primary: bool = False) -> None:
        self.meaning = meaning
        self.is_primary = is_primary


class Reading:
    def __init__(
        self, reading: str, reading_type: str, is_primary: bool = False
    ) -> None:
        self.reading = reading
        self.type = reading_type
        self.is_primary = is_primary


class BaseParser:
    def __init__(self):
        # Difficulty levels are used while parsing.
        # For example, a radicals list page have the next url:
        # https://wanikani.com/radicals?difficulty=pleasant
        self.difficulty_levels = [
            "pleasant",
            "painful",
            "death",
            "hell",
            "paradise",
            "reality",
        ]
        self.request_headers = settings.request_headers

        # Highlighting class names.
        self.radical_highlight_class_name = "radical-highlight"
        self.kanji_highlight_class_name = "kanji-highlight"
        self.reading_highlight_class_name = "reading-highlight"
        self.vocabulary_highlight_class_name = "vocabulary-highlight"

    async def _get_page_soup(self, page_url: str) -> BeautifulSoup:
        """
        Getting a page html and loading into a BeautifulSoup object.

        Parameters:
            page_url: str - the url of the page to load
        """
        async with aiohttp.ClientSession(headers=self.request_headers) as session:
            async with session.get(page_url) as resp:
                page_html = await resp.text()
                soup = BeautifulSoup(page_html, features="html.parser")
                return soup

    def _get_element_links(
        self, soup: BeautifulSoup, element_class_name: str
    ) -> list[str]:
        """
        Getting the all links from a page to a source page of a radical, kanji or word.
        The function requires the class name of the elements to search.
        The href parameter of the found elements will be returned.

        Parameters:
            soup: BeautifulSoup - the page soup
            element_class_name : str - the class name of the element to find

        Returns:
            element_urls: list[str] - the list of the urls to the pages of the radicals, kanji or words.
        """
        element_urls = []

        ol_elements = soup.find_all("a", class_=element_class_name)

        for element_li in ol_elements:
            element_page_url = element_li.get("href")
            element_urls.append(element_page_url)

        return element_urls

    def _get_element_meanings(self, soup: BeautifulSoup) -> list[Meaning]:
        """
        Get the element meanings.
        Element is understood as kanji or word,
        since kanji and word pages have the same layout for meaning blocks.
        One element can have multiple meanings: one primary meaning and some alternative meanings.
        For example, https://www.wanikani.com/vocabulary/%E4%B8%8A.

        Parameters:
            soup: BeautifulSoup - BeautifulSoup object.

        Returns:
            list[Meaning] - list of the meanings.
        """
        meanings = []

        for div_meaning in soup.find_all("div", class_="subject-section__meanings"):
            meaning_type = div_meaning.find(
                "h2", class_="subject-section__meanings-title"
            ).text
            meaning_text = div_meaning.find(
                "p", class_="subject-section__meanings-items"
            ).text

            if meaning_type == "Primary":
                meanings.append(Meaning(meaning=meaning_text, is_primary=True))
            elif meaning_type != "WordType":
                meanings.extend(
                    [Meaning(meaning=meaning) for meaning in meaning_text.split(", ")]
                )

        return meanings

    def _get_highlighted_words(
        self, soup: BeautifulSoup, tag_name: str, class_name: str
    ) -> list[str]:
        """
        Getting all the highlighted words from a soup.

        Args:
            soup: BeautifulSoup - the soup
            class_name: str - the class name of the div

        Returns:
            list[str] - the list of highlighted words
        """
        highlighted_words = []

        for element in soup.find_all(tag_name, class_=class_name):
            highlighted_words.append(element.text)

        return highlighted_words

    def _get_highlighted_radicals(self, soup: BeautifulSoup) -> list[str]:
        """
        Getting the highlighted radicals from the soup.
        """
        return self._get_highlighted_words(
            soup, "span", self.radical_highlight_class_name
        )

    def _get_highlighted_kanji(self, soup: BeautifulSoup) -> list[str]:
        """
        Getting the highlighted kanji from the soup.
        """
        return self._get_highlighted_words(
            soup, "span", self.kanji_highlight_class_name
        )

    def _get_highlighted_vocabulary(self, soup: BeautifulSoup) -> list[str]:
        """
        Get the highlighted vocabulary from the soup.
        """
        return self._get_highlighted_words(
            soup, "span", self.vocabulary_highlight_class_name
        )

    def _get_highlighted_readings(self, soup: BeautifulSoup) -> list[str]:
        """
        Getting the highlighted readings from the soup.
        """
        return self._get_highlighted_words(
            soup, "span", self.reading_highlight_class_name
        )

    def _get_element_level(self, soup: BeautifulSoup) -> int:
        """
        Getting the radical, kanji or word level from the soup.
        """
        return soup.find(
            "a", class_="page-header__icon page-header__icon--level"
        ).text.strip()

    def _get_mnemonic(self, soup, mnemonic_section_class: str) -> Mnemonic:
        """
        Getting the mnemonic of kanji, radicals or word from the soup.
        All mnemonics use the same classes for mnemonic text and hint,
        but some mnemonics can have not only one mnemonic on page,
        kanji, for example, have two mnemonics: one for reading and one for meaning.
        If page can have multiple mnemonics, then it's needed to pass the part of the page,
        where is only one mnemonic. Also, mnemonic can have note, so function returns Mnemonic object,
        which contains the note too.

        Returns:
            Mnemonic: Mnemonic class object.
        """
        mnemonic_section = soup.find("section", class_=mnemonic_section_class)

        mnemonic = ""

        for mnemonic_p in mnemonic_section.find_all(
            "p", class_="subject-section__text"
        ):
            mnemonic += mnemonic_p.text

        hint = mnemonic_section.find("p", class_="subject-hint__text")

        if hint:
            hint = hint.text
        else:
            hint = ""

        return Mnemonic(mnemonic=mnemonic, hint=hint)

    def _highlight_text(self, text: str, word_to_highlight: str) -> str:
        """
        Highlights the word to highlight in the text.

        Parameters:
            text: str - text
            word_to_highlight: str - the word to highlight

        Returns:
            highlighted_text: str - the highlighted text
        """
        highlighted_text = text.replace(word_to_highlight, word_to_highlight.upper())
        return highlighted_text

    def _download_file(self, file_path_to_save: str, file_url: str) -> None:
        """
        Downloads the file from the provided url.
        File will be saved in the file_path_to_save.

        Parameters:
            file_path_to_save: str - file path to save.
            file_url: str - file url to download from.

        Returns:
            None
        """
        with open(file_path_to_save, "wb") as audio_file:
            audio_file.write(requests.get(file_url).content)
