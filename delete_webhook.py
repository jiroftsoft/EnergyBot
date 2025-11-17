"""Quick script to delete Telegram webhook if one exists."""
import asyncio
from aiogram import Bot

# Token from .env or you can set it directly here
TOKEN = "8473642133:AAEKhqsc-cnwu08fybfgSZHPFHNpFvu7zNI"


async def main():
    bot = Bot(token=TOKEN)
    try:
        result = await bot.delete_webhook(drop_pending_updates=True)
        print(f"Webhook deleted: {result}")
        print("✅ You can now start the bot with: python -m app.telegram.main")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

