import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from fetch import fetch_today_messages
from summarizer import generate_summary
from discord_notifier import send_summary_to_discord
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()  # Registers slash commands globally
        print(f"🌍 Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@bot.tree.command(name="sendsummary", description="Fetch, summarize, and post today's cross-platform messages.")
async def sendsummary_command(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    # Fetch messages
    slack = fetch_today_messages("slack_messages")
    discord_msgs = fetch_today_messages("discord_messages")
    telegram = fetch_today_messages("telegram_messages")

    # Generate and post summary
    summary = generate_summary(slack, discord_msgs, telegram)
    send_summary_to_discord(summary)

    await interaction.followup.send("✅ Summary has been posted to the summary channel!")

bot.run(TOKEN)
