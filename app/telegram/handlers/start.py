from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.telegram.keyboards.main_menu import build_main_menu
from app.services.subscriptions import get_or_create_user, get_session

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Welcome the user, ensure they exist in DB, and show the main menu.
    """
    session = get_session()
    try:
        get_or_create_user(
            session=session,
            telegram_id=str(message.from_user.id),
            full_name=message.from_user.full_name,
        )
    finally:
        session.close()

    await state.clear()

    welcome_text = (
        "سلام 👋\n"
        "به ربات مدیریت باشگاه انرژی خوش آمدید.\n\n"
        "از منوی زیر می‌توانید پروفایل خود را تکمیل کنید، اشتراک بخرید و برنامه تمرینی/غذایی بگیرید. 🌟"
    )

    await message.answer(
        text=welcome_text,
        reply_markup=build_main_menu(),
    )

