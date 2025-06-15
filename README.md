# Multi-Platform Chat Summarizer

A backend service that listens to messages across **Discord**, **Slack**, and **Telegram** servers, stores them in a **PostgreSQL** database, and responds to the `/sendsummary` command from a Discord bot with a per-platform, per-channel summary of all recent conversations.

---

## Features

- Real-time ingestion of messages from Discord, Slack, and Telegram
- PostgreSQL-backed message archiving
- Summarisation on demand via a Discord slash command
- Separate summaries per app and per channel
- Built with **FastAPI**, **SQLAlchemy**, and **asyncio**
