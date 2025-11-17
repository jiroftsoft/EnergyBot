from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import User, SubscriptionPlan, Subscription


def get_session() -> Session:
    return SessionLocal()


def get_user_by_telegram_id(session: Session, telegram_id: str) -> Optional[User]:
    return session.query(User).filter(User.telegram_id == telegram_id).first()


def create_user(session: Session, telegram_id: str, full_name: Optional[str]) -> User:
    user = User(
        telegram_id=telegram_id,
        full_name=full_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_or_create_user(session: Session, telegram_id: str, full_name: Optional[str]) -> User:
    user = get_user_by_telegram_id(session, telegram_id)
    if user is None:
        user = create_user(session, telegram_id, full_name)
    return user


def update_user_profile(
    session: Session,
    user: User,
    *,
    gender: Optional[str] = None,
    age: Optional[int] = None,
    height_cm: Optional[float] = None,
    weight_kg: Optional[float] = None,
    goal: Optional[str] = None,
    user_type: Optional[str] = None,
) -> User:
    if gender is not None:
        user.gender = gender
    if age is not None:
        user.age = age
    if height_cm is not None:
        user.height_cm = height_cm
    if weight_kg is not None:
        user.weight_kg = weight_kg
    if goal is not None:
        user.goal = goal
    if user_type is not None:
        user.user_type = user_type

    session.commit()
    session.refresh(user)
    return user


def get_active_plans(session: Session) -> list[SubscriptionPlan]:
    return (
        session.query(SubscriptionPlan)
        .filter(SubscriptionPlan.is_active.is_(True))
        .order_by(SubscriptionPlan.category, SubscriptionPlan.duration_days)
        .all()
    )


def get_active_plans_for_user_type(session: Session, user_type: str) -> list[SubscriptionPlan]:
    """
    Return plans that the user is allowed to see.

    Strategy:
    - Always include 'normal' plans.
    - Additionally include plans whose category equals the user_type (if not 'normal').
    """
    q = session.query(SubscriptionPlan).filter(SubscriptionPlan.is_active.is_(True))
    plans = q.all()

    allowed: list[SubscriptionPlan] = []

    for plan in plans:
        if plan.category == "normal":
            allowed.append(plan)
        elif plan.category == user_type:
            allowed.append(plan)

    # If user has unknown type, just return normal plans
    if not allowed and user_type not in {"normal", "student", "employee"}:
        allowed = [p for p in plans if p.category == "normal"]

    # sort by category then duration
    allowed.sort(key=lambda p: (p.category, p.duration_days))
    return allowed


def activate_subscription(
    session: Session,
    user: User,
    plan: SubscriptionPlan,
    *,
    start: Optional[datetime] = None,
) -> Subscription:
    """
    Create a new active subscription for the user based on the plan.

    Deactivate previous active subscriptions that overlap, if desired.
    """
    if start is None:
        start = datetime.utcnow()

    end = start + timedelta(days=plan.duration_days)

    # Optionally, deactivate previous active subscriptions
    existing_active = (
        session.query(Subscription)
        .filter(
            Subscription.user_id == user.id,
            Subscription.is_active.is_(True),
        )
        .all()
    )
    for sub in existing_active:
        sub.is_active = False

    subscription = Subscription(
        user_id=user.id,
        plan_id=plan.id,
        start_date=start,
        end_date=end,
        is_active=True,
    )
    session.add(subscription)
    session.commit()
    session.refresh(subscription)
    return subscription

