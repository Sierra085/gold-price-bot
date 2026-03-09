import os
import sys
from datetime import datetime, timezone
import requests


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables", file=sys.stderr)
        sys.exit(1)

    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    message = f"Gold bot test message from GitHub Actions\n{utc_now}"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Failed to send message:", e, file=sys.stderr)
        sys.exit(1)

    print("Message sent. Telegram response:", resp.text)


if __name__ == "__main__":
    main()
