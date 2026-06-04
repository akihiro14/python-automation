import logging
import random
import time
from datetime import datetime
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://quotes.toscrape.com"
START_PATH = "/js"
USER_AGENT = "Mozilla/5.0 (compatible; QuoteScraper/1.0)"

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


def save_markdown(quotes: list[dict], output_path: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# 名言一覧 ({today})",
        "",
        f"収集件数: {len(quotes)} 件",
        "",
        "| 名言 | 著者 |",
        "| --- | --- |",
    ]
    for q in quotes:
        text = q["text"].replace("|", "｜")
        author = q["author"].replace("|", "｜")
        lines.append(f"| {text} | {author} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    logger.info("Markdown を保存しました: %s", output_path)


def main() -> None:
    rp = load_robots(BASE_URL)

    today = datetime.now().strftime("%Y%m%d")
    md_path = f"quotes_{today}.md"
    png_path = f"quotes_{today}.png"

    all_quotes: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()

        current_path = START_PATH
        page_num = 1

        while current_path:
            current_url = BASE_URL + current_path

            if not is_allowed(rp, current_url):
                logger.warning("robots.txt によりアクセス禁止: %s", current_url)
                break

            logger.info("ページ %d を取得中: %s", page_num, current_url)

            try:
                page.goto(current_url, timeout=15000)
                # JS描画完了を待つ
                page.wait_for_selector("div.quote", timeout=10000)
            except PlaywrightTimeoutError:
                logger.error("タイムアウト: %s", current_url)
                raise SystemExit(1)
            except Exception as e:
                logger.error("接続エラー: %s", e)
                raise SystemExit(1)

            # 1ページ目のみスクリーンショットを保存
            if page_num == 1:
                page.screenshot(path=png_path, full_page=True)
                logger.info("スクリーンショットを保存しました: %s", png_path)

            # 名言を取得
            quote_elements = page.query_selector_all("div.quote")
            for el in quote_elements:
                text = el.query_selector("span.text").inner_text().strip()
                author = el.query_selector("small.author").inner_text().strip()
                all_quotes.append({"text": text, "author": author})

            logger.info("  %d 件取得 (累計: %d 件)", len(quote_elements), len(all_quotes))

            # 次のページリンクを確認
            next_btn = page.query_selector("li.next a")
            if next_btn:
                current_path = next_btn.get_attribute("href")
                wait = random.uniform(1, 3)
                logger.info("  %.1f 秒待機します...", wait)
                time.sleep(wait)
                page_num += 1
            else:
                current_path = None

        browser.close()

    save_markdown(all_quotes, md_path)


if __name__ == "__main__":
    main()
