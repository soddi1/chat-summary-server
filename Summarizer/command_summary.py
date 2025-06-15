import discord
from discord.ext import commands
from discord import app_commands

from fetch import fetch_today_messages
from summarizer import generate_summary
from discord_notifier import send_summary_to_discord

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="sendsummary", description="Generate and send today's summary")
async def send_summary(interaction: discord.Interaction):
    await interaction.response.defer()  # Optional: shows "thinking..." while processing

    # Fetch and summarize messages
    slack = fetch_today_messages("slack_messages")
    discord_msgs = fetch_today_messages("discord_messages")
    telegram = fetch_today_messages("telegram_messages")
    summary = generate_summary(slack, discord_msgs, telegram)

    # Print in console (optional)
    print("\n📋 Summary:\n")
    print(summary)

    # Send to Discord channel
    send_summary_to_discord(summary)

    await interaction.followup.send("✅ Summary has been generated and sent!")

bot.run("DISCORD_BOT_TOKEN")
