import os
import requests
from datetime import datetime, timezone

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

if __name__ == "__main__":
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    try:
        r = requests.get(
            URL,
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            },
        )
        msg = (
            f"Gold bot diagnostics\n"
            f"Time: {now}\n"
            f"HTTP status: {r.status_code}\n"
            f"Final URL: {r.url}\n"
            f"Content length: {len(r.text)}\n\n"
            f"First 500 chars:\n{r.text[:500]}"
        )
    except Exception as e:
        msg = f"Gold bot diagnostics failed\nTime: {now}\nError: {e}"

    send_telegram(msg)