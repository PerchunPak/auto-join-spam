import asyncio

import telethon.tl.types
from loguru import logger

from src import utils
from src.config import Config
from src.db import Database
from src.extract_data import extract_data


def main() -> None:
    utils.setup_logging()
    logger.info("Hello World!")

    config = Config()
    Database()
    logger.info("Starting app...")
    with telethon.TelegramClient("data/bot", config.api_id, config.api_hash) as client:
        client.loop.run_until_complete(loop(client))


async def loop(client: telethon.TelegramClient) -> None:
    logger.info("Starting loop")
    db = Database()
    while True:
        if len(db.data["all_links"]) == 0:
            logger.info("DB is empty, initializing it")
            links, delayed_messages = await extract_data(client)

            db.add_links(links)
            for to, messages in delayed_messages.items():
                db.add_delayed_messages(messages, to=to)

        await asyncio.sleep(10)


if __name__ == "__main__":
    main()
