"""Simple Discord bridge for Requiem.

This bot relays messages between a Discord server and the running Requiem
instance exposed via ``web.py``. It expects the web server to provide the
``/api/discord`` endpoint which accepts a JSON payload ``{"message": "..."}``
and returns ``{"reply": "..."}``.

Usage::

    export DISCORD_TOKEN="your-bot-token"
    # Optional: where the web server lives and API auth token
    export REQUIEM_URL="http://localhost:5000/api/discord"
    export DISCORD_API_TOKEN="shared-secret"
    python discord_bot.py

The bot requires ``discord.py`` and ``requests``.
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

try:  # pragma: no cover - optional dependency
    import discord  # type: ignore
except Exception:  # pragma: no cover
    discord = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import requests
except Exception:  # pragma: no cover
    requests = None  # type: ignore


class RequiemDiscordBot(discord.Client if discord else object):
    """Minimal Discord client that forwards messages to Requiem."""

    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - runtime
        if discord is None or requests is None:
            raise ImportError("discord.py and requests are required to run the bot")
        intents = kwargs.pop("intents", discord.Intents.default())
        intents.message_content = True
        super().__init__(*args, intents=intents, **kwargs)
        self.api_url = os.environ.get("REQUIEM_URL", "http://localhost:5000/api/discord")
        self.api_token = os.environ.get("DISCORD_API_TOKEN")

    async def on_ready(self) -> None:  # pragma: no cover - network
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message: "discord.Message") -> None:  # pragma: no cover - network
        if message.author.id == self.user.id:
            return
        payload = {"message": message.content}
        headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
        loop = asyncio.get_running_loop()

        def call_api() -> Optional[str]:
            try:
                resp = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
                resp.raise_for_status()
                return resp.json().get("reply", "")
            except Exception:
                return None

        reply = await loop.run_in_executor(None, call_api)
        if reply:
            await message.channel.send(reply)


def main() -> None:  # pragma: no cover - runtime
    if discord is None:
        raise ImportError("discord.py is required to run the bot")
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable not set")
    bot = RequiemDiscordBot()
    bot.run(token)


if __name__ == "__main__":  # pragma: no cover - runtime
    main()
