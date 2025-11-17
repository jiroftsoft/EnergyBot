from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_main_menu() -> ReplyKeyboardMarkup:
    """
    Build the main reply keyboard for users.
    """
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text="📝 پروفایل من"),
        KeyboardButton(text="💳 خرید اشتراک"),
    )

    builder.row(
        KeyboardButton(text="📅 وضعیت اشتراک"),
    )

    builder.row(
        KeyboardButton(text="🏋️‍♀️ برنامه تمرینی"),
        KeyboardButton(text="🍎 برنامه غذایی"),
    )

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)

