import os
import requests
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # Required for Socket Mode
API_URL = "http://localhost:8000/slack"  # Your FastAPI endpoint

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

@app.event("message")
def handle_message_events(body, logger):
    """Handle incoming messages from all channels"""
    event = body["event"]
    
    # Skip bot messages and message subtypes (like file uploads, etc.)
    if event.get("bot_id") or event.get("subtype"):
        return
    
    # Get channel info
    channel_id = event["channel"]
    try:
        channel_info = app.client.conversations_info(channel=channel_id)
        channel_name = channel_info["channel"]["name"]
    except Exception as e:
        channel_name = channel_id
        logger.error(f"Could not get channel info: {e}")
    
    # Get user info
    user_id = event["user"]
    try:
        user_info = app.client.users_info(user=user_id)
        username = user_info["user"]["real_name"] or user_info["user"]["name"]
    except Exception as e:
        username = user_id
        logger.error(f"Could not get user info: {e}")
    
    # Convert timestamp to ISO format
    timestamp = float(event["ts"])
    date_iso = datetime.fromtimestamp(timestamp).isoformat()
    
    # Prepare payload
    payload = {
        "sender": username,
        "channel_name": channel_name,
        "message": event["text"],
        "date": date_iso
    }
    
    # Send to API
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"Message saved: {payload['message'][:50]}...")
        else:
            print(f"Failed to save: {response.text}")
    except Exception as e:
        print(f"Error sending to API: {e}")

@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    """Handle when the bot is mentioned (optional)"""
    event = body["event"]
    say(f"Hello <@{event['user']}>! I'm listening to messages.")

def main():
    """Start the Slack bot"""
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("✅ Slack bot is running...")
    handler.start()

if __name__ == "__main__":
    main()