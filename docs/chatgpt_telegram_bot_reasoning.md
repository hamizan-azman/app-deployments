# chatgpt_telegram_bot. Reasoning Log

## Initial Assessment

chatgpt_telegram_bot connects ChatGPT to Telegram. It is a bot process (no HTTP server) that uses the python-telegram-bot library to receive messages, forwards them to the OpenAI API, and sends responses back. Conversation history is stored in MongoDB to support multi-turn conversations. The project ships with a docker-compose.yml that brings up the bot, MongoDB, and Mongo Express together.

## What Was Checked

1. **README.md**: Describes setup as a three-container compose stack. Requires creating a `config/config.env` file with TELEGRAM_TOKEN and OPENAI_API_KEY before starting. Lists all supported bot commands and configuration options.

2. **Upstream Dockerfile**: Single-stage, python:3.8-slim. Installs ffmpeg and build tools, upgrades pip/wheel/setuptools, installs requirements.txt, creates non-root user appuser, copies code, and runs bot/bot.py.

3. **docker-compose.yml**: Defines three services: bot (using the built image), mongodb (mongo:latest), and mongo-express (for DB inspection). Bot service mounts config/config.env as an env file.

4. **requirements.txt**: Includes python-telegram-bot, openai, pymongo, and audio/image processing libraries.

5. **bot/bot.py**: Main bot process. Reads configuration from environment variables. Connects to MongoDB on startup.

## Decisions Made

### Used the existing Dockerfile as-is

The upstream Dockerfile is minimal and correct. It creates a non-root user, installs ffmpeg, and runs the bot. No modifications were needed.

### Python 3.8 preserved

The upstream pins Python 3.8. This is intentional. The version of python-telegram-bot used by this project has compatibility constraints that prevent running on Python 3.11+. The upstream made this choice deliberately and it was preserved per the architectural fidelity rule.

### Kept the compose structure

The docker-compose.yml defines the full stack including MongoDB. The bot depends on MongoDB for conversation history storage. Removing MongoDB would require modifying the application's storage layer, which violates the architectural fidelity rule. The compose file is provided as-is.

### Kept config/config.env approach

The upstream design uses a config.env file mounted into the container. This is a deliberate separation of secrets from the image. API keys are never baked into the image. The compose file references this file with `env_file: config/config.env`.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. All system packages installed. Python dependencies from requirements.txt resolved under Python 3.8.
2. **Telegram import**: `python -c "import telegram"` passed. This is the healthcheck.
3. **Container startup**: Bot process started. Exited immediately with "TELEGRAM_TOKEN not set" error (expected without config.env).

### What Was Not Tested
- Actual Telegram bot operation (requires a valid TELEGRAM_TOKEN and OPENAI_API_KEY)
- MongoDB connection and conversation persistence
- Voice message transcription
- Image generation via DALL-E

## Gotchas

1. **config/config.env must exist before compose up**: Docker Compose will fail to start the bot service if the config/config.env file does not exist at the path referenced in the compose file. Create the file with at minimum TELEGRAM_TOKEN and OPENAI_API_KEY before running compose.

2. **Python 3.8 end of life**: Python 3.8 reached end of life in October 2024. It no longer receives security patches. This is an upstream constraint. For research deployments this is acceptable but should be noted for any production use.

3. **No HTTP port on the bot container**: The bot has no web interface and no health endpoint. The healthcheck uses a Python import test rather than an HTTP request. Monitoring the bot requires checking Docker logs or the Mongo Express UI.

4. **MongoDB startup order**: The bot will attempt to connect to MongoDB at startup. If MongoDB is not yet ready, the bot may fail to start or retry. The compose file should include a depends_on with a health condition for MongoDB if startup ordering is critical.

5. **setuptools pinned to 59.5.0**: The upstream pins setuptools at this specific version to avoid breaking changes in newer setuptools versions that affect some packages in the requirements list.
