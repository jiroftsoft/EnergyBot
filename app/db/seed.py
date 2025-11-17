from typing import Iterable

from sqlalchemy.orm import Session

from app.db.models import SubscriptionPlan


def seed_subscription_plans(session: Session) -> None:
    """
    Insert default subscription plans if they do not already exist.
    """
    defaults: list[dict] = [
        {
            "name": "اشتراک ۱ ماهه",
            "code": "1m_normal",
            "duration_days": 30,
            "category": "normal",
            "price": 500000,
            "description": "اشتراک عادی یک ماهه",
        },
        {
            "name": "اشتراک ۲ ماهه",
            "code": "2m_normal",
            "duration_days": 60,
            "category": "normal",
            "price": 900000,
            "description": "اشتراک عادی دو ماهه",
        },
        {
            "name": "اشتراک ۳ ماهه",
            "code": "3m_normal",
            "duration_days": 90,
            "category": "normal",
            "price": 1300000,
            "description": "اشتراک عادی سه ماهه",
        },
        {
            "name": "اشتراک ۶ ماهه",
            "code": "6m_normal",
            "duration_days": 180,
            "category": "normal",
            "price": 2400000,
            "description": "اشتراک عادی شش ماهه",
        },
        {
            "name": "پلن دانشجویی ۱ ماهه",
            "code": "1m_student",
            "duration_days": 30,
            "category": "student",
            "price": 350000,
            "description": "اشتراک ویژه دانشجویان",
        },
        {
            "name": "پلن کارمندی ۱ ماهه",
            "code": "1m_employee",
            "duration_days": 30,
            "category": "employee",
            "price": 400000,
            "description": "اشتراک ویژه کارمندان",
        },
    ]

    for data in defaults:
        existing = session.query(SubscriptionPlan).filter_by(code=data["code"]).first()
        if not existing:
            session.add(SubscriptionPlan(**data))

    session.commit()


def run_initial_seed() -> None:
    from app.db.session import SessionLocal

    session = SessionLocal()
    try:
        seed_subscription_plans(session)
    finally:
        session.close()

