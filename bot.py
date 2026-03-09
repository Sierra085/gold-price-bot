import os
import re
import requests
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://goldprice.org/live-gold-price.html"


def send_telegram(message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()


def parse_first_big_price(text: str) -> float:
    candidates = re.findall(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b", text)
    values = []
    for c in candidates:
        try:
            v = float(c.replace(",", ""))
            if 1000 <= v <= 10000:
                values.append(v)
        except ValueError:
            pass

    if not values:
        raise ValueError("No plausible gold price found in page text.")

    return values[0]


def fetch_usd_oz_gold() -> float:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)

        body_text = page.locator("body").inner_text()
        browser.close()

    return parse_first_big_price(body_text)


if __name__ == "__main__":
    price = fetch_usd_oz_gold()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    message = (
        "Gold Update\n\n"
        "USD\n"
        f"- oz: {price:,.2f}\n\n"
        f"Updated: {now}"
    )

    send_telegram(message)