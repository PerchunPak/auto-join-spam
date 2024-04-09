import telethon
from loguru import logger
from src.db import Database


class RateLimitError(Exception):
    sleep_for: int


def sanitize_link(link: str) -> str:
    assert link.startswith("https://t.me/+"), link
    return link.removeprefix("https://t.me/+")


async def join_all_links(client: telethon.TelegramClient, links: set[str]) -> None:
    db = Database()
    links = links.copy()

    for link in links:
        logger.info("Joining {}...", link)

        try:
            result = await client(
                telethon.functions.messages.ImportChatInviteRequest(
                    hash=sanitize_link(link)
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

        else:
            logger.critical(f"Cannot join {link}: {result.stringify()!r}")


async def send_delayed_messages(delayed_messages: dict[int, set[str]]) -> None:
    pass
