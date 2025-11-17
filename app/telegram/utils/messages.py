import asyncio
import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, Message, ReplyKeyboardMarkup

logger = logging.getLogger(__name__)


async def _delete_later(
    bot: Bot,
    chat_id: int,
    message_id: int,
    delay_seconds: int,
) -> None:
    await asyncio.sleep(delay_seconds)
    with suppress(TelegramBadRequest):
        await bot.delete_message(chat_id=chat_id, message_id=message_id)


async def send_temp_message(
    bot: Bot,
    chat_id: int,
    text: str,
    *,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    delete_after: int = 60,
) -> Message:
    """
    Send a message that will be automatically deleted after delete_after seconds.
    """
    msg = await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    asyncio.create_task(_delete_later(bot, chat_id, msg.message_id, delete_after))
    return msg

