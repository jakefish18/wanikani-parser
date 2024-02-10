import requests
import logging
logging.basicConfig(level=logging.INFO, filename="logs/wk_radical_parser.log", filemode="w")

from src.crud import CrudWKRadical
from src.parsers.base import BaseParser
from src.models import WKRadical
from src.database import SessionLocal
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

    def run(self, is_download_image: bool = False) -> None:

        """
        Run the parser.
        """
        for difficulty_level in self.difficulty_levels:
            radical_list_page_url = f"{settings.WANIKANI_BASE_URL}/radicals?difficulty={difficulty_level}"
            soup = self._get_page_soup(radical_list_page_url)
            radical_page_urls = self._get_element_links(soup, self.radicals_page_link_class)
            total_radical_count = len(radical_page_urls)

            for i, radical_page_url in enumerate(radical_page_urls):
                self._parse_radical_page(radical_page_url, is_download_image=is_download_image)
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

        level = self._get_element_level(soup)
        meaning = soup.find("p", class_="subject-section__meanings-items").text.strip()
        mnemonic = soup.find("p", class_="subject-section__text").text.strip()

        symbol = soup.find("span", class_="page-header__icon page-header__icon--radical").text.strip()
        symbol_image_url = soup.find("wk-character-image", class_="radical-image").get("src")
        # Symbol is stored as an image, if it's WaniKani custom radical.
        if symbol_image_url and is_download_image:
            with open(f"output/images/{meaning}.svg", "wb") as image_file:
                image_file.write(requests.get(symbol_image_url).content)

        # Highlighting radical meaning in mnemonic with the upper case.
        highlighted_radicals = self._get_highlighted_radicals(soup)

        for highlighted_radicals in highlighted_radicals:
            mnemonic = self._highlight_text(mnemonic, highlighted_radicals)

        with SessionLocal() as db:
            wk_radical = WKRadical(
                level=int(level),
                symbol=symbol,
                meaning=meaning,
                mnemonic=mnemonic,
                is_symbol_image=bool(symbol_image_url)
            )
            self.crud_wk_radical.create(db, wk_radical)


if __name__ == "__main__":
    # Parsing and saving all the radicals into the csv file.
    wk_radicals_parser = WKRadicalsParser()
    wk_radicals_parser.run(is_download_image=False)