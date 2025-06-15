from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_summary(slack_msgs, discord_msgs, telegram_msgs):
    def format_platform_messages(msgs, platform_name):
        """Group messages by channel and format them consistently"""
        if not msgs:
            return f"{platform_name}:\nNo messages found.\n"
        
        # Group messages by channel
        channels = {}
        for msg in msgs:
            channel = msg['channel_name']
            if channel not in channels:
                channels[channel] = []
            channels[channel].append(msg)
        
        # Sort channels alphabetically for consistent ordering
        sorted_channels = sorted(channels.keys())
        
        # Format messages for each channel
        formatted_text = f"{platform_name}:\n"
        for channel in sorted_channels:
            channel_msgs = channels[channel]
            formatted_text += f"\n#{channel}:\n"
            for msg in channel_msgs:
                formatted_text += f"  - {msg['sender']}: {msg['message']}\n"
        
        return formatted_text + "\n"
    
    # Format messages for each platform
    slack_text = format_platform_messages(slack_msgs, "Slack")
    discord_text = format_platform_messages(discord_msgs, "Discord")
    telegram_text = format_platform_messages(telegram_msgs, "Telegram")
    
    # Debug prints (consider using logging instead)
    print("=== SLACK MESSAGES ===")
    print(slack_text)
    print("=== DISCORD MESSAGES ===")
    print(discord_text)
    print("=== TELEGRAM MESSAGES ===")
    print(telegram_text)
    
    # Construct prompt with clear structure
    prompt = (
        f"{HUMAN_PROMPT} You are to act as a day-to-day summarizer. My company uses three communication applications: Discord, Slack, and Telegram. "
        f"You will receive today's messages grouped by channel for each application. Your job is to summarize all updates and return a detailed **per-channel** summary for each application. Your job is to only summarize, not add on any opinion of your own into the summary.\n\n"
        
        f"<rules>\n"
        f"- Ignore casual greetings like 'Hello' or 'Hi'\n"
        f"- Focus only on meaningful content, updates, or discussions\n"
        f"- Summaries should be around 40% of original text length (not less)\n"
        f"- Specify who did what task\n"
        f"- Include all important information - the reader hasn't seen the original messages\n"
        f"- Highlight tasks assigned and to whom\n"
        f"- When in doubt about importance, include the information\n"
        f"- Do not include channels where there was nothing important done!\n"
        f"- Again do not mention any greetings!\n"
        f"</rules>\n\n"
        f"Messages by Platform and Channel:\n\n"
        f"{slack_text}"
        f"{discord_text}"
        f"{telegram_text}"

        f"Required Output Format:\n\n"
        f"<output_format>"
        f"Slack:\n"
        f" - #channel-name: [detailed summary of that specific channel's messages]\n"
        f" - #another-channel: [detailed summary of that specific channel's messages]\n\n"
        f"Discord:\n"
        f" - #channel-name: [detailed summary of that specific channel's messages]\n\n"
        f"Telegram:\n"
        f" - #channel-name: [detailed summary of that specific channel's messages]\n\n"
        f"Ensure each summary corresponds exactly to the messages from that specific channel listed above.\n"
        f"</output_format>\n\n"
        f"{AI_PROMPT}"
    )
    
    # return prompt

    # Send to Claude
    response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

    return response.content[0].text.strip()

# def main():
#     # Sample test data
#     slack_messages = [
#         {
#             "sender": "John",
#             "channel_name": "general",
#             "message": "Team meeting scheduled for tomorrow at 10 AM"
#         },
#         {
#             "sender": "Sarah",
#             "channel_name": "general",
#             "message": "I've updated the project timeline in the shared doc"
#         },
#         {
#             "sender": "Mike",
#             "channel_name": "tech-updates",
#             "message": "New API endpoints are now live in production"
#         }
#     ]

#     discord_messages = [
#         {
#             "sender": "Alex",
#             "channel_name": "announcements",
#             "message": "New feature release: User authentication system"
#         },
#         {
#             "sender": "Emma",
#             "channel_name": "support",
#             "message": "Resolved critical bug in payment processing"
#         }
#     ]

#     telegram_messages = [
#         {
#             "sender": "David",
#             "channel_name": "updates",
#             "message": "Server maintenance completed successfully"
#         },
#         {
#             "sender": "Lisa",
#             "channel_name": "updates",
#             "message": "Database backup completed"
#         }
#     ]

#     # Generate summary
#     summary = generate_summary(slack_messages, discord_messages, telegram_messages)
#     print("Generated Summary:")
#     print(summary)

# if __name__ == "__main__":
#     main()

