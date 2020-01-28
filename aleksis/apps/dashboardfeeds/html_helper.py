from bs4 import BeautifulSoup


def parse_rss_html(rss_html: str) -> (str, str):
    soup = BeautifulSoup(rss_html)

    rich_text = soup.get_text()
    img_href = soup.img
    if img_href:
        img_href = img_href.get("src", None)

    return rich_text, img_href
