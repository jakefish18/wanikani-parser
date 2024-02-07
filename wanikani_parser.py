import requests
import csv
import logging
logging.basicConfig(filename="output/logs.log", level=logging.INFO, filemode="w")

from bs4 import BeautifulSoup

from models import WaniKaniRadical


def get_page_soup(url: str) -> BeautifulSoup:
    """
    Getting page soup.

    Parameters:
        url: str - page url
    Returns:
        soup: BeautifulSoup - soup
    """
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    response = requests.get(url, headers=request_headers)
    page_html = response.text
    soup = BeautifulSoup(page_html, features="html.parser")
    return soup

def wanikani_radicals_parser(is_save_to_csv: bool = False, is_download_images: bool = False) -> list[WaniKaniRadical]:
    """
    Function for parsing all radicals from wanikani.
    Returns the list of WaniKani radicals.
    Every radical in list contain its symbol, name and mnemonic.
    """
    wanikani_radicals = []

    soup = get_page_soup("https://www.wanikani.com/radicals")

    ol_radicals = soup.find_all("a", class_="subject-character subject-character--radical subject-character--grid subject-character--unlocked")
    radicals_count = len(ol_radicals)

    for radical_li in ol_radicals:
        radical_page_url = radical_li.get("href")
        wanikani_radical = wanikani_radical_page_parser(radical_page_url)

        wanikani_radicals.append(wanikani_radical)
        logging.info(f"Processed {radical_page_url} [{len(wanikani_radicals)}/{radicals_count}]")

    if is_save_to_csv:
        save_to_csv(wanikani_radicals)
        return []

    else:
        return wanikani_radicals


def wanikani_radical_page_parser(radical_page_url: str, is_download_image: bool = True) -> WaniKaniRadical:
    """
    Function for parsing radical info from page.

    Parameters:
        radical_page_url: str - page of the radical to parse

    Returns:
        WaniKaniRadical object
    """
    try:
        soup = get_page_soup(radical_page_url)

        meaning = soup.find("p", class_="subject-section__meanings-items").text.strip()
        mnemonic = soup.find("p", class_="subject-section__text").text.strip()
        level = soup.find("a", class_="page-header__icon page-header__icon--level").text.strip()

        symbol = soup.find("span", class_="page-header__icon page-header__icon--radical").text.strip()
        # Symbol stored as image, if it's WaniKani custom radical.
        if not symbol:
            logging.warning(f"{radical_page_url} has no symbol")

            # Downloading image.
            symbol_image_element = soup.find("wk-character-image", class_="radical-image")
            image_url = symbol_image_element.get("src")

            if is_download_image:
                with open(f"output/images/{meaning}.svg", "wb") as image_file:
                    image_file.write(requests.get(image_url).content)

            resize_image(f"output/images/{meaning}.svg", 32, 32)
            symbol = f'<img src="{meaning}.svg">'

        # Highlighting radical meaning in mnemonic with upper case.
        try:
            mnemonic_highlight = soup.find("span", class_="radical-highlight").text.strip()
            mnemonic = mnemonic.replace(mnemonic_highlight, mnemonic_highlight.upper())
        except:
            logging.warning(f"{radical_page_url} haven't mnemonic")

        return WaniKaniRadical(
            level=level,
            symbol=symbol,
            meaning=meaning,
            mnemonic=mnemonic
        )

    except:
        logging.critical(msg=f"{radical_page_url} went wrong")
        raise FileNotFoundError

def save_to_csv(wanikani_radicals: list[WaniKaniRadical]) -> None:
    """
    Saving all wanikani radicals into the csv file.

    Parameters:
        wanikani_radicals: list[WaniKaniRadical] - radicals to save into the csv file.
    """
    with open("output/wanikani_radicals.csv", "w", newline="", encoding="utf-8") as file:
        csvwriter = csv.writer(file, delimiter=";")

        for wanikani_radical in wanikani_radicals:
            row = [wanikani_radical.level, wanikani_radical.symbol, wanikani_radical.meaning, wanikani_radical.mnemonic]
            csvwriter.writerow(row)


def import_from_csv() -> list[WaniKaniRadical]:
    """
    Importing all WaniKani radicals from the csv file instead of parsing from zero.
    """
    wanikani_radicals = []

    with open("output/wanikani_radicals.csv", "r", newline="", encoding="utf-8") as file:
        csvreader = csv.reader(file)

        for row in csvreader:
            wanikani_radicals.append(WaniKaniRadical(
                level=row[0],
                symbol=row[1],
                meaning=row[2],
                mnemonic=row[3]
            ))

    return wanikani_radicals


if __name__ == "__main__":
    # Parsing and saving all the radicals into the csv file.
    wanikani_radicals_parser(is_save_to_csv=True, is_download_images=True)