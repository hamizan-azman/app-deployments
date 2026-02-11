# chatgpt_telegram_bot. Usage Documentation

## Overview
Telegram bot that connects ChatGPT to Telegram conversations. Stores conversation history in MongoDB and supports voice messages via ffmpeg transcription. Includes Mongo Express for database inspection.

## Quick Start
```bash
docker pull hoomzoom/chatgpt-telegram-bot

# Create config directory and config file
mkdir -p config
cat > config/config.env << 'EOF'
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
EOF

# Run with docker-compose (recommended, includes MongoDB)
cd dockerfiles/chatgpt_telegram_bot
docker-compose up -d
```

## Services (docker-compose)

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| bot | hoomzoom/chatgpt-telegram-bot | None | Telegram bot process |
| mongodb | mongo:latest | 27017 (internal) | Conversation history storage |
| mongo-express | mongo-express | 8081 | MongoDB web UI |

Mongo Express is available at http://localhost:8081 (credentials: admin / password, or as set in compose).

## Core Features
- Full ChatGPT conversation support in Telegram chats and groups
- Persistent conversation history stored in MongoDB
- Voice message support via ffmpeg audio transcription
- Support for multiple simultaneous users
- Image generation via DALL-E (requires valid API key)

## Health Check
The Dockerfile healthcheck runs `python -c "import telegram"` to verify the python-telegram-bot package is installed and importable.

## Configuration
All configuration is via `config/config.env`. This file must be mounted into the container at `/code/config/config.env`.

| Variable | Required | Description |
|----------|----------|-------------|
| TELEGRAM_TOKEN | Yes | Bot token from @BotFather on Telegram |
| OPENAI_API_KEY | Yes | OpenAI API key for ChatGPT and DALL-E |
| ALLOWED_TELEGRAM_USERNAMES | No | Comma-separated whitelist of usernames |
| MONGODB_URI | No | MongoDB connection string (default: mongodb://mongodb:27017) |

## Notes
- The bot requires a valid Telegram token and OpenAI key before it will connect. It will fail to start without both.
- Python 3.8 is used (pinned by upstream). The python-telegram-bot library version in this project requires Python 3.8.
- ffmpeg is installed for voice message support. Voice transcription requires an OpenAI API key with Whisper access.
- The container runs as non-root user `appuser` (UID 1000).
- The bot process has no HTTP port. There is no web UI for the bot itself. Monitor it via docker logs.

## Changes from Original
No changes to the Dockerfile structure. The Dockerfile was already minimal and correct.

## V2 Dependency Changes
Minimum version pinning applied to requirements.txt. All minimum versions resolved successfully without bumps.
