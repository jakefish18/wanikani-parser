import requests

from bs4 import BeautifulSoup

from src.core import settings


class BaseParser:
    def __init__(self):
        # Difficulty levels are used while parsing.
        # For example, a radicals list page have the next url:
        # https://wanikani.com/radicals?difficulty=pleasant
        self.difficulty_levels = ["pleasant", "painful", "death", "hell", "paradise", "reality"]
        self.request_headers = settings.request_headers

    def _get_page_soup(self, page_url: str) -> BeautifulSoup:
        """
        Getting a page html and loading into a BeautifulSoup object.

        Parameters:
            page_url: str - the url of the page to load
        """
        response = requests.get(page_url, headers=self.request_headers)
        page_html = response.text
        soup = BeautifulSoup(page_html, features="html.parser")
        return soup

    def _get_element_links(self, soup: BeautifulSoup, element_class_name: str) -> list[str]:
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

        for radical_li in ol_elements:
            radical_page_url = radical_li.get("href")
            element_urls.append(radical_page_url)

        return element_urls

    def _get_highlighted_words(self, soup: BeautifulSoup, tag_name: str, class_name: str) -> list[str]:
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