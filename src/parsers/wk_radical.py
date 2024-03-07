import asyncio
import logging

from src.core import settings
from src.crud import CrudWKRadical
from src.database import SessionLocal
from src.models import WKRadical
from src.parsers.base import BaseParser


class WKRadicalsParser(BaseParser):
    def __init__(self):
        super().__init__()

        # The class names of the spans which are highlighted in the mnemonics.
        self.meaning_highlight_tag = "span"
        self.meaning_highlight_class = "radical-highlight"

        # The class name of the "a" tag which has link to the radical page.
        self.radicals_page_link_class = (
            "subject-character subject-character--radical "
            "subject-character--grid subject-character--unlocked"
        )

        self.crud_wk_radical = CrudWKRadical(WKRadical)

    def run(self, is_download_image: bool = False) -> None:
        """
        Run the parser.
        """
        tasks = []

        for difficulty_level in self.difficulty_levels:
            radical_list_page_url = (
                f"{settings.WANIKANI_BASE_URL}/radicals?difficulty={difficulty_level}"
            )
            soup = self._get_page_soup(radical_list_page_url)
            radical_page_urls = self._get_element_links(
                soup, self.radicals_page_link_class
            )
            total_radical_count = len(radical_page_urls)

            for i, radical_page_url in enumerate(radical_page_urls):
                if not self._is_radical_exists(radical_page_url):
                    tasks.append(
                        asyncio.create_task(
                            self._parse_radical_page(
                                radical_page_url,
                                i,
                                total_radical_count,
                                is_download_image=is_download_image,
                            )
                        )
                    )
                else:
                    logging.warning(
                        f"{radical_page_url} already exists in the database."
                    )

    def _is_radical_exists(self, url: str) -> bool:
        """Checking if radical exists in the database by its url."""
        with SessionLocal() as db:
            return self.crud_wk_radical.is_radical_by_url(db, url)

    async def _parse_radical_page(
        self,
        radical_page_url: str,
        i: int,
        total_radical_count: int,
        is_download_image: bool = True,
    ) -> WKRadical:
        """
        Parsing the radical info from page.

        Parameters:
            radical_page_url: str - page of the radical to parse

        Returns:
            WaniKaniRadical object
        """
        soup = await self._get_page_soup(radical_page_url)

        level = await self._get_element_level(soup)
        meaning = soup.find("p", class_="subject-section__meanings-items").text.strip()
        mnemonic = soup.find("p", class_="subject-section__text").text.strip()

        symbol = soup.find(
            "span", class_="page-header__icon page-header__icon--radical"
        ).text.strip()

        # Symbol is stored as an image, if it's WaniKani custom radical.
        symbol_image_url = ""
        symbol_image_element = soup.find("wk-character-image", class_="radical-image")

        if symbol_image_element:
            symbol_image_url = symbol_image_element.get("src")

            if is_download_image:
                self._download_file(symbol_image_url, f"output/images/{meaning}.svg")

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
                is_symbol_image=bool(symbol_image_url),
                url=radical_page_url,
            )
            self.crud_wk_radical.create(db, wk_radical)

        logging.info(f"Processed {radical_page_url} [{i}/{total_radical_count}]")


if __name__ == "__main__":
    # Parsing and saving all the radicals into the csv file.
    wk_radicals_parser = WKRadicalsParser()
    wk_radicals_parser.run(is_download_image=False)
