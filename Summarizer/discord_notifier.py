import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_summary_to_discord(summary_text: str):
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Missing DISCORD_WEBHOOK_URL in environment!")

    data = {
        "content": f"**Daily Communication Summary**\n\n{summary_text}"
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Summary sent to Discord!")
    else:
        print("Failed to send summary:", response.status_code, response.text)
