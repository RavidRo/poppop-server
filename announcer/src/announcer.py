import asyncio
import logging
import threading
from typing import Any, Optional

import discord
from discord import Intents, TextChannel

from mclogging import logger, setup_logs
from mcqueue import Queue

DISCORD_TOKEN = "ODcyNzEzNzQwMzA1NDYxMjk5.YQt4AQ.99TCVbpXqNJXl2ULSyvnXRZ6EZI"


class Consumer:
    def __init__(self, queue: asyncio.Queue[str]) -> None:
        self.messages_queue = queue

    def run(self) -> None:
        with Queue() as q:
            q.listen(self._on_message)

    def _on_message(self, body: str) -> None:
        self.messages_queue.put_nowait(body)


class Announcer(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.mc_channel: Optional[TextChannel] = None
        self.messages_queue: asyncio.Queue[str] = asyncio.Queue()
        self.consumer = Consumer(self.messages_queue)

    async def on_ready(self) -> None:
        logger.info(f"Logged on as {self.user}!")

        for channel in self.get_all_channels():
            if channel.name == "mc-server":
                if channel.type == discord.ChannelType.text:
                    self.mc_channel = channel
                    asyncio.create_task(self._listen())
                    return
                else:
                    raise Exception("mc-server channel is not a text channel")
        raise Exception("mc-server channel not found")

    async def _listen(self) -> None:
        consumer_thread = threading.Thread(target=self.consumer.run)
        consumer_thread.start()

        while True:
            message = await self.messages_queue.get()
            await self.mc_channel.send(message)
            logger.info(f"Announced message: {message}")


def run_bot() -> None:
    logger.info("Starting announcer...")

    intents = discord.Intents.default()
    intents.message_content = True

    client = Announcer(intents=intents)
    client.run(
        token=DISCORD_TOKEN,
        reconnect=True,
        log_level=logging.INFO,
    )


if __name__ == "__main__":
    setup_logs("announcer")
    run_bot()
