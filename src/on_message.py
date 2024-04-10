import telethon.events
import telethon.tl.types
from loguru import logger
from src.extract_data import extract_message
from src.db import Database


def register(client: telethon.TelegramClient) -> None:
    client.on(telethon.events.NewMessage())(on_message)
    logger.trace("Registered hooks")


async def on_message(event: telethon.events.NewMessage.Event) -> None:
    db = Database()
    sender = (
        event.message.sender
        if event.message.sender is not None
        else await event.message.get_sender()
    )

    # if not a user/bot OR if not a channel
    if (not isinstance(sender, (telethon.tl.types.User)) or not sender.bot) or (
        not isinstance(sender, telethon.tl.types.Channel)
    ):
        logger.trace("Got invalid message from {} (not a bot/channel)", sender)
        return

    links_to_add, messages_to_add = await extract_message(event.message)
    logger.info(
        f"New message from: {sender.username} (links: {len(links_to_add)}; delayed messages: {len(messages_to_add)})"
    )

    db.add_links(links_to_add)
    db.add_delayed_messages(messages_to_add, to=sender.id)
