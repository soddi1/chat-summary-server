import logging
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8000/telegram"  # Your FastAPI endpoint

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and send them to the API."""
    message = update.message
    
    # Skip if no message
    if not message:
        return
    
    # Skip bot messages (optional, similar to Discord version)
    if message.from_user.is_bot:
        return
    
    print("Message: ", message)
    
    # Get sender information
    sender = message.from_user.full_name or message.from_user.username or f"User_{message.from_user.id}"
    
    # Get channel/chat information
    if message.chat.type == 'private':
        channel_name = f"DM with {sender}"
    elif message.chat.title:
        channel_name = message.chat.title
    else:
        channel_name = f"Chat_{message.chat.id}"
    
    # Prepare payload
    payload = {
        "sender": sender,
        "channel_name": channel_name,
        "message": message.text or "[Non-text message]",
        "date": message.date.isoformat(),
        "chat_id": message.chat.id,
        "user_id": message.from_user.id
    }
    
    # Send to API
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Message saved:", payload["message"])
        else:
            print("Failed to save:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error sending to API: {e}")

def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    print("🔍 Testing bot token...")
    
    # Create the Application with network settings
    application = (Application.builder()
                  .token(TELEGRAM_BOT_TOKEN)
                  .connect_timeout(30)
                  .read_timeout(30)
                  .write_timeout(30)
                  .pool_timeout(30)
                  .build())
    
    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add handler for all other message types (photos, documents, etc.)
    application.add_handler(MessageHandler(~filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Starting Telegram bot...")
    
    try:
        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Possible solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify your TELEGRAM_BOT_TOKEN is correct")
        print("   3. Try using a VPN if Telegram is blocked in your region")
        print("   4. Check if your firewall is blocking the connection")

if __name__ == '__main__':
    main()