# AGENTS.md

## Project Overview

Telegram bot for managing card decks (Vampire: The Eternal Struggle). Uses Pyrogram for Telegram, masonite-orm for SQLite database.

## Developer Commands

```bash
# Install dependencies
uv sync

# Lint (ruff + blue)
task lint

# Format (blue + isort)
task format

# Run bot
python -m gehennabot.main

# Run CLI commands
python -m gehennabot.cli <command>
```

Available CLI commands: `procura-carta`, `procura-carta-id`, `adicionar`, `falta`, `falta-e-procura`, `decks`, `usuarios`, `preconstruidos`, `adicionar-precon`, plus `gehenna-api-*` commands that hit `localhost:8002`.

## Key Files

- `gehennabot/main.py` - Bot entry point
- `gehennabot/cli.py` - CLI commands (typer)
- `gehennabot/service.py` - Business logic
- `gehennabot/api.py` - External API calls
- `config/database.py` - Masonite ORM config
- `.env` - Required env vars (TOKEN_API, API_ID, API_HASH, DATABASE_URL)

## Notes

- Package manager is `uv`, NOT poetry (Makefile is outdated)
- Database is SQLite, path from `DATABASE_URL` in `.env`
- Some CLI commands require external API at `localhost:8002`
- No test suite visible
- Python 3.11-3.14 supported