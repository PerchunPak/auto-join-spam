import telethon.tl.types
from loguru import logger


async def extract_data_from_bots(
    client: telethon.TelegramClient,
) -> tuple[set[str], dict[int, set[str]]]:
    links: set[str] = set()
    delayed_messages: dict[int, set[str]] = {}
    async for dialog in client.iter_dialogs():
        if not dialog.is_user or not dialog.entity.bot:
            continue
        logger.debug(f"Extracting links from {dialog.name}...")

        messages_to_send: set[str] = set()
        async for message in client.iter_messages(dialog):
            links_to_add, messages_to_add = await extract_message(message)
            links.update(links_to_add)
            messages_to_send.update(messages_to_add)

        delayed_messages.setdefault(dialog.id, set())
        delayed_messages[dialog.id].update(messages_to_send)

    return links, delayed_messages


async def extract_data_from_unread_messages(
    client: telethon.TelegramClient,
) -> tuple[set[str], dict[int, set[str]]]:
    links: set[str] = set()
    delayed_messages: dict[int, set[str]] = {}
    async for dialog in client.iter_dialogs():
        if dialog.unread_count == 0:
            continue
        logger.info(f"Found unread messages in {dialog.name}")

        messages_to_send: set[str] = set()
        async for message in client.iter_messages(
            dialog, limit=dialog.unread_count, reverse=True
        ):
            links_to_add, messages_to_add = await extract_message(message)
            links.update(links_to_add)
            messages_to_send.update(messages_to_add)

        await client.send_read_acknowledge(dialog)

        delayed_messages.setdefault(dialog.id, set())
        delayed_messages[dialog.id].update(messages_to_send)

    return links, delayed_messages


async def extract_message(
    message: telethon.types.Message,
) -> tuple[set[str], set[str]]:
    links: set[str] = set()
    messages_to_send: set[str] = set()
    if message.entities is not None:
        links.update(
            extract_links_from_entities(message.message, message.entities)
        )

    if message.reply_markup is not None:
        messages_to_add, links_to_add = extract_links_from_reply_markup(
            message.reply_markup
        )

        links.update(links_to_add)
        messages_to_send.update(messages_to_add)

    return links, messages_to_send


def extract_links_from_entities(
    msg: str,
    entities: list[telethon.tl.types.TypeMessageEntity],
) -> set[str]:
    result: set[str] = set()
    for entity in entities:
        if not isinstance(
            entity,
            (
                telethon.tl.types.MessageEntityTextUrl,
                telethon.tl.types.MessageEntityUrl,
            ),
        ):
            continue

        if isinstance(entity, telethon.tl.types.MessageEntityTextUrl):
            result.add(entity.url)
        else:
            result.add(msg[entity.offset : entity.offset + entity.length])

    return result


def extract_links_from_reply_markup(
    reply_markup: telethon.tl.types.TypeReplyMarkup,
) -> tuple[set[str], set[str]]:
    """
    Returns:
        Two sets: messages to send and links.
    """
    # no `.rows`
    assert not isinstance(
        reply_markup,
        (
            telethon.tl.types.ReplyKeyboardForceReply,
            telethon.tl.types.ReplyKeyboardHide,
        ),
    )

    messages_to_add: set[str] = set()
    links_to_add: set[str] = set()

    for row in reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, telethon.tl.types.KeyboardButtonUrl):
                links_to_add.add(button.url)
            elif isinstance(button, telethon.tl.types.KeyboardButton):
                messages_to_add.add(button.text)

    return messages_to_add, links_to_add
