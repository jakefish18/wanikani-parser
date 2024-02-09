import requests
import csv
import logging
logging.basicConfig(level=logging.INFO, filename="logs/wk_radical_parser.log", filemode="w")

from bs4 import BeautifulSoup

from src.crud import CrudWKRadical
from src.parsers.base import BaseParser
from src.models import WKRadical
from src.database import SessionLocal, engine
from src.core import settings


class WKRadicalsParser(BaseParser):
    def __init__(self):
        super().__init__()

        # The class names of the spans which are highlighted in the mnemonics.
        self.meaning_highlight_tag = "span"
        self.meaning_highlight_class = "radical-highlight"

        # The class name of the "a" tag which has link to the radical page.
        self.radicals_page_link_class = ("subject-character subject-character--radical "
                                         "subject-character--grid subject-character--unlocked")

        self.crud_wk_radical = CrudWKRadical(WKRadical)

    def run(self):
        """
        Run the parser.
        """
        for difficulty_level in self.difficulty_levels:
            radical_list_page_url = f"{settings.WANIKANI_BASE_URL}/radicals?difficulty={difficulty_level}"
            soup = self._get_page_soup(radical_list_page_url)
            radical_page_urls = self._get_element_links(soup, self.radicals_page_link_class)
            total_radical_count = len(radical_page_urls)

            for i, radical_page_url in enumerate(radical_page_urls):
                self._parse_radical_page(radical_page_url, is_download_image=True)
                logging.info(f"Processed {radical_page_url} [{i + 1}/{total_radical_count}]")
    def _parse_radical_page(self, radical_page_url: str, is_download_image: bool = True) -> WKRadical:
        """
        Parsing the radical info from page.

        Parameters:
            radical_page_url: str - page of the radical to parse

        Returns:
            WaniKaniRadical object
        """
        soup = self._get_page_soup(radical_page_url)

        meaning = soup.find("p", class_="subject-section__meanings-items").text.strip()
        mnemonic = soup.find("p", class_="subject-section__text").text.strip()
        level = soup.find("a", class_="page-header__icon page-header__icon--level").text.strip()

        symbol = soup.find("span", class_="page-header__icon page-header__icon--radical").text.strip()
        # Symbol is stored as an image, if it's WaniKani custom radical.
        if not symbol:
            # Downloading an image.
            symbol_image_element = soup.find("wk-character-image", class_="radical-image")
            image_url = symbol_image_element.get("src")

            if is_download_image:
                with open(f"output/images/{meaning}.svg", "wb") as image_file:
                    image_file.write(requests.get(image_url).content)

            symbol = f'<img src="{meaning}.svg">'

        # Highlighting radical meaning in mnemonic with the upper case.
        highlighted_words = self._get_highlighted_words(soup, self.meaning_highlight_tag, self.meaning_highlight_class)

        for highlighted_word in highlighted_words:
            mnemonic = self._highlight_text(mnemonic, highlighted_word)

        with SessionLocal() as db:
            wk_radical = WKRadical(
                level=int(level),
                symbol=symbol,
                meaning=meaning,
                mnemonic=mnemonic
            )
            self.crud_wk_radical.create(db, wk_radical)


if __name__ == "__main__":
    # Parsing and saving all the radicals into the csv file.
    wk_radicals_parser = WKRadicalsParser()
    wk_radicals_parser.run()