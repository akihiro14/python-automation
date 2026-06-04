import logging
import random
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "Mozilla/5.0 (compatible; BookScraper/1.0)"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def load_robots(base_url: str) -> RobotFileParser:
    rp = RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        rp.set_url(robots_url)
        rp.read()
        logger.info("robots.txt を読み込みました: %s", robots_url)
    except Exception as e:
        logger.warning("robots.txt の読み込みに失敗しました: %s", e)
    return rp


def is_allowed(rp: RobotFileParser, url: str) -> bool:
    return rp.can_fetch(USER_AGENT, url)


def fetch(session: requests.Session, url: str) -> BeautifulSoup | None:
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.ConnectionError as e:
        logger.error("接続エラー: %s", e)
        raise SystemExit(1)
    except requests.exceptions.HTTPError as e:
        logger.error("HTTPエラー: %s", e)
        raise SystemExit(1)
    except requests.exceptions.Timeout:
        logger.error("タイムアウト: %s", url)
        raise SystemExit(1)


def parse_books(soup: BeautifulSoup) -> list[dict]:
    books = []
    for article in soup.select("article.product_pod"):
        title = article.select_one("h3 a")["title"]
        price = article.select_one("p.price_color").text.strip()
        availability = article.select_one("p.availability").text.strip()
        books.append({"title": title, "price": price, "availability": availability})
    return books


def get_next_page_url(soup: BeautifulSoup, current_url: str) -> str | None:
    next_btn = soup.select_one("li.next a")
    if not next_btn:
        return None
    # current_url のディレクトリ基準で相対パスを解決
    base = current_url.rsplit("/", 1)[0] + "/"
    return urljoin(base, next_btn["href"])


def save_markdown(books: list[dict], output_path: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# 書籍一覧 ({today})",
        "",
        f"収集件数: {len(books)} 件",
        "",
        "| タイトル | 価格 | 在庫状況 |",
        "| --- | --- | --- |",
    ]
    for book in books:
        title = book["title"].replace("|", "｜")
        lines.append(f"| {title} | {book['price']} | {book['availability']} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    logger.info("保存しました: %s", output_path)


def main() -> None:
    rp = load_robots(BASE_URL)

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    all_books: list[dict] = []
    current_url = BASE_URL
    page = 1

    while current_url:
        if not is_allowed(rp, current_url):
            logger.warning("robots.txt によりアクセス禁止: %s", current_url)
            break

        logger.info("ページ %d を取得中: %s", page, current_url)
        soup = fetch(session, current_url)

        books = parse_books(soup)
        all_books.extend(books)
        logger.info("  %d 件取得 (累計: %d 件)", len(books), len(all_books))

        current_url = get_next_page_url(soup, current_url)
        page += 1

        if current_url:
            wait = random.uniform(1, 3)
            logger.info("  %.1f 秒待機します...", wait)
            time.sleep(wait)

    today = datetime.now().strftime("%Y%m%d")
    output_path = f"books_{today}.md"
    save_markdown(all_books, output_path)


if __name__ == "__main__":
    main()
