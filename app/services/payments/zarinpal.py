from __future__ import annotations

import json
import logging
from typing import Optional, Tuple

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Payment, SubscriptionPlan, User
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

# Base URLs for sandbox vs production
if settings.ZARINPAL_SANDBOX:
    ZARINPAL_API_BASE = "https://sandbox.zarinpal.com/pg/v4/payment"
    ZARINPAL_STARTPAY_BASE = "https://sandbox.zarinpal.com/pg/StartPay"
else:
    ZARINPAL_API_BASE = "https://api.zarinpal.com/pg/v4/payment"
    ZARINPAL_STARTPAY_BASE = "https://www.zarinpal.com/pg/StartPay"


def get_session() -> Session:
    return SessionLocal()


async def _post_json(url: str, payload: dict) -> dict:
    """
    Send a JSON POST request to Zarinpal and return the parsed JSON.
    Raise httpx.HTTPError on network failures.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            url,
            json=payload,
            headers={"accept": "application/json", "content-type": "application/json"},
        )
        resp.raise_for_status()
        return resp.json()


async def create_payment_for_plan(
    user_id: int,
    plan_id: int,
    session: Optional[Session] = None,
) -> str:
    """
    Create a Payment record for the given user and plan,
    call Zarinpal's payment request API, store authority, and
    return the payment URL for redirect.

    Uses:
    - settings.ZARINPAL_MERCHANT_ID
    - settings.ZARINPAL_CALLBACK_URL
    """
    if not settings.ZARINPAL_MERCHANT_ID:
        raise RuntimeError("ZARINPAL_MERCHANT_ID is not configured")
    if not settings.ZARINPAL_CALLBACK_URL:
        raise RuntimeError("ZARINPAL_CALLBACK_URL is not configured")

    owns_session = False
    if session is None:
        session = get_session()
        owns_session = True

    try:
        user: User | None = session.query(User).filter(User.id == user_id).first()
        plan: SubscriptionPlan | None = session.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
        if user is None or plan is None:
            raise ValueError("User or plan not found")

        amount = plan.price  # Amount in Tomans
        description = f"EnergyGym subscription: {plan.name} - user #{user.id}"

        # Create local payment row with pending status
        payment = Payment(
            user_id=user.id,
            plan_id=plan.id,
            amount=amount,  # Store in Tomans
            gateway="zarinpal",
            status="pending",
        )
        session.add(payment)
        session.commit()
        session.refresh(payment)

        # Build Zarinpal request payload (v4 JSON API)
        # Zarinpal expects amount in Rials, so multiply by 10
        amount_rials = amount * 10
        payload = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount_rials,
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
            "description": description,
            # You could include metadata such as mobile/email if stored:
            # "metadata": {"mobile": "...", "email": "..."},
        }

        try:
            data = await _post_json(f"{ZARINPAL_API_BASE}/request.json", payload)
        except httpx.HTTPError as exc:
            logger.exception("Error calling Zarinpal request API: %s", exc)
            payment.status = "failed"
            payment.raw_response = f"http_error: {exc}"
            session.commit()
            raise RuntimeError("خطا در ارتباط با درگاه زرین‌پال، لطفاً بعداً دوباره تلاش کنید.")

        # Expected response format (from docs):
        # { "data": {"code": 100, "message": "...", "authority": "..."}, "errors": {...}? }
        raw_json = json.dumps(data, ensure_ascii=False)
        payment.raw_response = raw_json

        resp_data = data.get("data") or {}
        code = resp_data.get("code")
        authority = resp_data.get("authority")

        if code != 100 or not authority:
            # Error case
            error_message = (data.get("errors") or {}).get("message") or "خطا در ایجاد تراکنش."
            logger.error("Zarinpal request failed: code=%s errors=%s", code, data.get("errors"))
            payment.status = "failed"
            session.commit()
            raise RuntimeError(f"خطا در ایجاد پرداخت: {error_message}")

        # Success: store authority and keep status pending
        payment.authority = authority
        session.commit()
        session.refresh(payment)

        payment_url = f"{ZARINPAL_STARTPAY_BASE}/{authority}"
        logger.info(
            "Created payment: id=%s user_id=%s plan_id=%s amount=%s authority=%s",
            payment.id,
            user.id,
            plan.id,
            amount,
            authority,
        )
        return payment_url
    finally:
        if owns_session:
            session.close()


async def verify_and_update_payment(
    session: Session,
    authority: str,
    status: str,
) -> Tuple[bool, Optional[Payment]]:
    """
    Verify a payment with Zarinpal after the user returns to callback URL.

    - If Status != "OK": mark payment as failed (if found) and return (False, payment or None).
    - If Status == "OK":
        - Find Payment by authority.
        - Call Zarinpal /verify.json with merchant_id, amount, authority.
        - If code == 100 or 101:
            - Mark payment.status = "success".
            - Set payment.ref_id from response.
        - Else:
            - Mark payment.status = "failed".
        - Save raw_response.
    Returns (success, payment or None).
    """
    if not authority:
        return False, None

    payment: Payment | None = (
        session.query(Payment)
        .filter(Payment.authority == authority)
        .first()
    )
    if payment is None:
        logger.warning("Payment with authority %s not found in DB", authority)
        return False, None

    if status != "OK":
        payment.status = "failed"
        session.commit()
        logger.info("Payment %s marked as failed due to Status=%s", payment.id, status)
        return False, payment

    if not settings.ZARINPAL_MERCHANT_ID:
        raise RuntimeError("ZARINPAL_MERCHANT_ID is not configured")

    # Zarinpal expects amount in Rials, so multiply by 10
    amount_rials = payment.amount * 10
    payload = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount_rials,
        "authority": authority,
    }

    try:
        data = await _post_json(f"{ZARINPAL_API_BASE}/verify.json", payload)
    except httpx.HTTPError as exc:
        logger.exception("Error calling Zarinpal verify API: %s", exc)
        payment.status = "failed"
        payment.raw_response = f"http_error: {exc}"
        session.commit()
        return False, payment

    raw_json = json.dumps(data, ensure_ascii=False)
    payment.raw_response = raw_json

    resp_data = data.get("data") or {}
    code = resp_data.get("code")
    ref_id = resp_data.get("ref_id")

    # According to docs, 100 = success, 101 = already verified
    if code in (100, 101):
        payment.status = "success"
        if ref_id:
            payment.ref_id = str(ref_id)
        session.commit()
        session.refresh(payment)
        logger.info("Payment %s verified successfully with code=%s", payment.id, code)
        return True, payment

    # Any other code is a failure
    logger.error("Zarinpal verify failed: code=%s data=%s", code, resp_data)
    payment.status = "failed"
    session.commit()
    return False, payment
