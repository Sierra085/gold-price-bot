import os
import requests
from datetime import datetime, timezone

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

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
    message = (
        "Gold Update\n\n"
        "USD\n"
        "- oz: 5,082.49\n"
        "- g: 163.41\n"
        "- kg: 163,410.00\n\n"
        "SGD\n"
        "- oz: 6,845.72\n"
        "- g: 220.10\n"
        "- kg: 220,100.00\n\n"
        f"Updated: {now}"
    )
    send_telegram(message)