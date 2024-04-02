import telethon.tl.types
from loguru import logger


async def extract_data(
    client: telethon.TelegramClient,
) -> tuple[set[str], dict[int, set[str]]]:
    links: set[str] = set()
    delayed_messages: dict[int, set[str]] = {}
    async for dialog in client.iter_dialogs():
        if not dialog.is_user or not dialog.entity.bot:
            continue

        messages_to_send: set[str] = set()
        async for message in client.iter_messages(dialog):
            logger.info(f"{dialog.name}")

            if message.entities is not None:
                links.update(
                    extract_links_from_entities(message.text, message.entities)
                )

            if message.reply_markup is not None:
                messages_to_add, links_to_add = extract_links_from_reply_markup(
                    message.reply_markup
                )

                links.update(links_to_add)
                messages_to_send.update(messages_to_add)

        delayed_messages.setdefault(dialog.id, set())
        delayed_messages[dialog.id].update(messages_to_send)

    return links, delayed_messages


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
    reply_markup: telethon.tl.types.ReplyInlineMarkup,
) -> tuple[set[str], set[str]]:
    """
    Returns:
        Two sets: messages to send and links.
    """
    messages_to_add: set[str] = set()
    links_to_add: set[str] = set()

    for row in reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, telethon.tl.types.KeyboardButtonUrl):
                links_to_add.add(button.url)
            elif isinstance(button, telethon.tl.types.KeyboardButton):
                messages_to_add.add(button.text)

    return messages_to_add, links_to_add
