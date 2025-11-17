from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.models import SubscriptionPlan


def build_subscription_plans_keyboard(plans: list[SubscriptionPlan]) -> InlineKeyboardMarkup:
    """
    Build inline keyboard where each button is a subscription plan.

    callback_data format: "buy_plan:{plan_id}"
    """
    builder = InlineKeyboardBuilder()
    for plan in plans:
        text = f"{plan.name} - {plan.price:,} تومان"
        builder.button(text=text, callback_data=f"buy_plan:{plan.id}")

    builder.adjust(1)
    return builder.as_markup()

