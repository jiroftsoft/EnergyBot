from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram import Bot

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db import init_db
from app.db.models import Payment
from app.db.session import SessionLocal
from app.services.payments.zarinpal import verify_and_update_payment

logger = logging.getLogger(__name__)

app = FastAPI(title="EnergyGym Admin")
templates = Jinja2Templates(directory="app/web_admin/templates")


@app.on_event("startup")
def on_startup() -> None:
    setup_logging()
    logger.info("Starting admin web app...")
    init_db()
    logger.info("Database initialized for admin web app.")


@app.get("/health", response_class=HTMLResponse)
async def health() -> str:
    return "OK"


@app.get("/zarinpal/callback", response_class=HTMLResponse)
async def zarinpal_callback(
    request: Request,
    Authority: Optional[str] = None,
    Status: Optional[str] = None,
) -> HTMLResponse:
    """
    Zarinpal will redirect the user to this endpoint after payment.
    """
    if Authority is None or Status is None:
        return HTMLResponse(
            content="<h3>پارامترهای بازگشت ناقص است.</h3>",
            status_code=400,
        )

    logger.info("Zarinpal callback: Authority=%s Status=%s", Authority, Status)

    session = SessionLocal()
    try:
        # 1) Verify with Zarinpal and update Payment row
        success, payment = await verify_and_update_payment(
            session=session,
            authority=Authority,
            status=Status,
        )

        if not success or payment is None:
            # اگر Authority=TEST باشد، این یک تست است
            if Authority and Authority.upper() == "TEST":
                return HTMLResponse(
                    content="<h3>✅ Callback به درستی کار می‌کند!</h3>"
                            "<p>این یک تست بود. Authority=TEST در دیتابیس وجود ندارد.</p>"
                            "<p>برای تست واقعی، یک پرداخت واقعی انجام دهید.</p>",
                    status_code=200,
                )
            
            # لاگ دقیق‌تر برای عیب‌یابی
            logger.error("Payment verification failed: Authority=%s, success=%s, payment=%s", 
                        Authority, success, payment is not None)
            
            error_msg = "<h3>پرداخت توسط درگاه تأیید نشد یا لغو شد.</h3>"
            if payment is None:
                error_msg += "<p>⚠️ Payment record در دیتابیس یافت نشد. ممکن است ربات در local اجرا شده باشد.</p>"
            return HTMLResponse(
                content=error_msg,
                status_code=200,
            )

        # 2) Activate subscription if there's a plan_id
        from app.db.models import User, SubscriptionPlan  # local import to avoid circular
        from app.services.subscriptions import activate_subscription

        message_html = ""
        user: User | None = session.query(User).filter(User.id == payment.user_id).first()
        plan: SubscriptionPlan | None = None
        if payment.plan_id is not None:
            plan = session.query(SubscriptionPlan).filter(SubscriptionPlan.id == payment.plan_id).first()

        if user and plan:
            activate_subscription(session=session, user=user, plan=plan)
            logger.info("Subscription activated for user_id=%s plan_id=%s", user.id, plan.id)
            message_html = "<h3>پرداخت با موفقیت انجام شد و اشتراک شما فعال شد ✅</h3>"
        else:
            message_html = "<h3>پرداخت با موفقیت انجام شد ✅</h3>"

        # 3) Optionally notify user on Telegram (non-critical)
        bot = None
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            if user is not None:
                chat_id = int(user.telegram_id)
                text = (
                    "پرداخت شما با موفقیت تأیید شد ✅\n"
                    f"پلن: {plan.name if plan else 'نامشخص'}\n"
                    "اشتراک شما در باشگاه فعال شد. 💪"
                )
                await bot.send_message(chat_id=chat_id, text=text)
        except Exception as notify_exc:
            logger.warning("Failed to send Telegram notification: %s", notify_exc)
        finally:
            if bot:
                await bot.session.close()

        return HTMLResponse(content=message_html, status_code=200)
    finally:
        session.close()

