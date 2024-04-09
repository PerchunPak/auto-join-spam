import asyncio
import random

import telethon
from loguru import logger

from src.db import Database


class RateLimitError(Exception):
    def __init__(self, sleep_for: int) -> None:
        self.sleep_for = sleep_for


async def join_all_links(client: telethon.TelegramClient, links: set[str]) -> None:
    db = Database()
    links = links.copy()

    for link in links:
        logger.info("Joining {}...", link)

        try:
            result = await client(
                telethon.functions.messages.ImportChatInviteRequest(
                    hash=link.removeprefix("+")
                )
            )

        except telethon.errors.InviteRequestSentError:
            db.mark_link_as_joined(link)
            logger.success(f"Successfully requested join to {link}")

        except telethon.errors.UserAlreadyParticipantError:
            db.mark_link_as_joined(link)
            logger.success(f"Apparently, we already joined {link}")

        except telethon.errors.FloodWaitError as error:
            raise RateLimitError(sleep_for=error.seconds)

        except telethon.errors.InviteHashExpiredError:
            db.mark_link_as_joined(link)
            logger.warning(f"Apparently, {link} has expired")

        else:
            logger.critical(f"Cannot join {link}: {result.stringify()!r}")

        to_sleep = 10 + random.randint(0, 10)
        logger.info(f"Sleeping for {to_sleep} seconds before trying other link")
        await asyncio.sleep(to_sleep)


async def send_delayed_messages(delayed_messages: dict[int, set[str]]) -> None:
    pass
