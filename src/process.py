import telethon
from loguru import logger


class RateLimitError(Exception): ...


async def join_all_links(client: telethon.TelegramClient, links: set[str]) -> None:
    for link in links:
        logger.info("Joining {}...", link)
        await client(telethon.functions.messages.ImportChatInviteRequest(link))


async def send_delayed_messages(delayed_messages: dict[int, set[str]]) -> None:
    pass
