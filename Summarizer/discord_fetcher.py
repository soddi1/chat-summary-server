import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_URL = "http://localhost:8000/discord"  # Your FastAPI endpoint

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    print("Message: ", message)
    if message.author.bot:
        return

    display_name = message.author.nick or message.author.global_name or message.author.name

    payload = {
        "sender": display_name,
        "channel_name": str(message.channel),
        "message": message.content,
        "date": message.created_at.isoformat()
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        print("Message saved:", payload["message"])
    else:
        print("Failed to save:", response.text)

client.run(DISCORD_BOT_TOKEN)
