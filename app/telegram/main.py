import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db import init_db


def create_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    from app.telegram.handlers.start import router as start_router
    from app.telegram.handlers.registration import router as registration_router
    from app.telegram.handlers.subscriptions import router as subscriptions_router
    from app.telegram.handlers.payments import router as payments_router
    from app.telegram.handlers.plans import router as plans_router

    dp.include_routers(
        start_router,
        registration_router,
        subscriptions_router,
        payments_router,
        plans_router,
    )

    return dp


async def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Telegram bot...")

    init_db()
    logger.info("Database initialized.")

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = create_dispatcher()

    logger.info("Bot polling started.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

