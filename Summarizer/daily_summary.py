from fetch import fetch_today_messages
from summarizer import generate_summary

if __name__ == "__main__":
    slack = fetch_today_messages("slack_messages")
    discord = fetch_today_messages("discord_messages")
    telegram = fetch_today_messages("telegram_messages")

    summary = generate_summary(slack, discord, telegram)
    print("📋 Daily Summary:\n")
    print(summary)
