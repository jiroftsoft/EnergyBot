from __future__ import annotations

from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message

from app.db.models import Subscription
from app.services.subscriptions import (
    get_active_plans_for_user_type,
    get_session,
    get_user_by_telegram_id,
)
from app.telegram.keyboards.subscriptions import build_subscription_plans_keyboard

router = Router()


@router.message(F.text == "💳 خرید اشتراک")
async def buy_subscription_menu(message: Message) -> None:
    session = get_session()
    try:
        user = get_user_by_telegram_id(session, str(message.from_user.id))
        if user is None:
            await message.answer("ابتدا با دستور /start وارد ربات شوید و پروفایل خود را تکمیل کنید.")
            return

        user_type = user.user_type or "normal"
        plans = get_active_plans_for_user_type(session, user_type=user_type)

        if not plans:
            await message.answer("در حال حاضر هیچ پلن فعالی برای عضویت تعریف نشده است.")
            return

        kb = build_subscription_plans_keyboard(plans)
        text = (
            "لطفاً یکی از پلن‌های عضویت را انتخاب کنید:\n\n"
            "پس از انتخاب پلن، به درگاه پرداخت هدایت می‌شوید. 💳"
        )
        await message.answer(text, reply_markup=kb)
    finally:
        session.close()


@router.message(F.text == "📅 وضعیت اشتراک")
async def subscription_status(message: Message) -> None:
    session = get_session()
    try:
        user = get_user_by_telegram_id(session, str(message.from_user.id))
        if user is None:
            await message.answer("ابتدا با دستور /start وارد ربات شوید.")
            return

        # Find latest subscription
        sub: Subscription | None = (
            session.query(Subscription)
            .filter(Subscription.user_id == user.id)
            .order_by(Subscription.start_date.desc())
            .first()
        )
        if sub is None:
            await message.answer("شما هنوز هیچ اشتراکی فعال نکرده‌اید.")
            return

        status_icon = "✅" if sub.is_active else "⏹"
        now = datetime.utcnow()
        remaining_days = None
        if sub.is_active and sub.end_date:
            remaining_days = (sub.end_date.date() - now.date()).days

        plan_name = sub.plan.name if sub.plan else "نامشخص"

        text_lines = [
            f"وضعیت اشتراک شما {status_icon}",
            f"پلن: {plan_name}",
            f"تاریخ شروع: {sub.start_date.strftime('%Y-%m-%d')}",
            f"تاریخ پایان: {sub.end_date.strftime('%Y-%m-%d')}",
        ]
        if remaining_days is not None:
            text_lines.append(f"روزهای باقی‌مانده: {remaining_days} روز")

        await message.answer("\n".join(text_lines))
    finally:
        session.close()
