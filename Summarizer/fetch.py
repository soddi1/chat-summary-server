from datetime import datetime, timezone
from supabase_client import supabase

def fetch_today_messages(table_name: str):
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)

    query = (
        supabase.table(table_name)
        .select("*")
        .gte("date", today_start.isoformat())
        .execute()
    )
    return query.data

# from datetime import datetime, timedelta, timezone

# def fetch_today_messages(table_name: str):
#     now = datetime.now(timezone.utc)
#     yesterday_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) - timedelta(days=1)
#     yesterday_end = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)

#     query = (
#         supabase.table(table_name)
#         .select("*")
#         .gte("date", yesterday_start.isoformat())
#         .lt("date", yesterday_end.isoformat())
#         .execute()
#     )
#     return query.data


if __name__ == "__main__":
    slack = fetch_today_messages("slack_messages")
    discord = fetch_today_messages("discord_messages")
    telegram = fetch_today_messages("telegram_messages")

    print("📨 Slack Messages:")
    for msg in slack:
        print(f"[{msg['date']}] {msg['sender']} in {msg['channel_name']}: {msg['message']}")

    print("\n📨 Discord Messages:")
    for msg in discord:
        print(f"[{msg['date']}] {msg['sender']} in {msg['channel_name']}: {msg['message']}")

    print("\n📨 Telegram Messages:")
    for msg in telegram:
        print(f"[{msg['date']}] {msg['sender']} in {msg['channel_name']}: {msg['message']}")
