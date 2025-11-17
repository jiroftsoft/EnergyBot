from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.services.payments.zarinpal import create_payment_for_plan
from app.services.subscriptions import get_session, get_user_by_telegram_id

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data.startswith("buy_plan:"))
async def process_buy_plan_callback(callback: CallbackQuery) -> None:
    data = callback.data or ""
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await callback.answer("درخواست نامعتبر است.", show_alert=True)
        return

    plan_id_str = parts[1]
    try:
        plan_id = int(plan_id_str)
    except ValueError:
        await callback.answer("پلن انتخاب‌شده نامعتبر است.", show_alert=True)
        return

    session = get_session()
    try:
        user = get_user_by_telegram_id(session, str(callback.from_user.id))
        if user is None:
            await callback.answer("ابتدا باید ثبت‌نام کنید.", show_alert=True)
            return

        # Create payment and get URL
        payment_url = await create_payment_for_plan(
            user_id=user.id,
            plan_id=plan_id,
            session=session,
        )

        # Build URL button
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="رفتن به درگاه پرداخت 💳",
                        url=payment_url,
                    )
                ]
            ]
        )

        await callback.message.answer(
            "برای تکمیل پرداخت روی دکمه زیر بزنید. بعد از پرداخت، منتظر تأیید ربات باشید. ✅",
            reply_markup=kb,
        )
        await callback.answer()  # close loading state
    except Exception as exc:
        logger.exception("Error while creating payment: %s", exc)
        await callback.answer("خطا در ایجاد پرداخت. لطفاً بعداً دوباره تلاش کنید.", show_alert=True)
    finally:
        session.close()
