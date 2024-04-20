import asyncio
from datetime import timedelta

import telethon.tl.types
from loguru import logger

from src import extract_data, on_message, process, utils
from src.config import Config
from src.db import Database


def main() -> None:
    utils.setup_logging()
    logger.info("Hello World!")

    config = Config()
    Database()
    logger.info("Starting app...")
    with telethon.TelegramClient("data/bot", config.api_id, config.api_hash) as client:
        on_message.register(client)
        client.loop.run_until_complete(loop(client))


async def loop(client: telethon.TelegramClient) -> None:
    logger.info("Starting loop")
    db = Database()
    utils.start_sentry()
    await utils.start_apykuma()

    if len(db.data["all_links"]) == 0:
        logger.info("DB is empty, initializing it")
        links, delayed_messages = await extract_data.extract_data_from_bots(client)
    else:
        links, delayed_messages = await extract_data.extract_data_from_unread_messages(client)

    db.add_links(links)
    for to, messages in delayed_messages.items():
        db.add_delayed_messages(messages, to=to)

    while True:
        try:
            await process.join_all_links(client, db.data["links"])
        except process.RateLimitError as error:
            logger.warning(f"Got rate limited for {timedelta(seconds=error.sleep_for)}! Sleeping for next 20 minutes")
        else:
            await process.send_delayed_messages(db.data["delayed_messages"])

        await asyncio.sleep(20 * 60)


if __name__ == "__main__":
    main()
