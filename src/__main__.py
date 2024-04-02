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
    while True:
        links, delayed_messages = await extract_data(client)

        print(links)
        print(delayed_messages)

        break


if __name__ == "__main__":
    main()
