from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from app.services.subscriptions import (
    get_session,
    get_user_by_telegram_id,
    update_user_profile,
)
from app.telegram.states.registration import RegistrationState
from app.telegram.utils.messages import send_temp_message

router = Router()


def gender_keyboard() -> ReplyKeyboardMarkup:
    from aiogram.utils.keyboard import ReplyKeyboardBuilder

    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="خانم"),
        KeyboardButton(text="آقا"),
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def goal_keyboard() -> ReplyKeyboardMarkup:
    from aiogram.utils.keyboard import ReplyKeyboardBuilder

    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="چربی‌سوزی"),
        KeyboardButton(text="عضله‌سازی"),
    )
    builder.row(
        KeyboardButton(text="تناسب اندام"),
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def user_type_keyboard() -> ReplyKeyboardMarkup:
    from aiogram.utils.keyboard import ReplyKeyboardBuilder

    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="عادی"),
    )
    builder.row(
        KeyboardButton(text="دانشجویی"),
        KeyboardButton(text="کارمندی"),
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


@router.message(F.text == "📝 پروفایل من")
async def start_profile_flow(message: Message, state: FSMContext) -> None:
    await state.set_state(RegistrationState.gender)
    question = (
        "ورزشکار عزیز ☺️\n"
        "لطفاً جنسیت خود را انتخاب کنید:"
    )
    await send_temp_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text=question,
        reply_markup=gender_keyboard(),
        delete_after=90,
    )


@router.message(RegistrationState.gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if text not in ("خانم", "آقا"):
        await send_temp_message(
            bot=message.bot,
            chat_id=message.chat.id,
            text="لطفاً فقط یکی از گزینه‌های موجود را انتخاب کنید 🌸",
            delete_after=20,
        )
        return

    gender_value = "female" if text == "خانم" else "male"
    await state.update_data(gender=gender_value)

    await state.set_state(RegistrationState.age)
    await send_temp_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text="سن شما چند سال است؟",
        delete_after=90,
    )


@router.message(RegistrationState.age)
async def process_age(message: Message, state: FSMContext) -> None:
    try:
        age = int((message.text or "").strip())
        if age < 10 or age > 80:
            raise ValueError()
    except ValueError:
        await send_temp_message(
            bot=message.bot,
            chat_id=message.chat.id,
            text="لطفاً سن را به عدد صحیح بین ۱۰ تا ۸۰ وارد کنید 🙏",
            delete_after=20,
        )
        return

    await state.update_data(age=age)
    await state.set_state(RegistrationState.height)
    await send_temp_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text="قد خود را به سانتی‌متر وارد کنید (مثلاً 165).",
        delete_after=90,
    )


@router.message(RegistrationState.height)
async def process_height(message: Message, state: FSMContext) -> None:
    try:
        height = float((message.text or "").strip())
        if height < 120 or height > 230:
            raise ValueError()
    except ValueError:
        await send_temp_message(
            bot=message.bot,
            chat_id=message.chat.id,
            text="قد را به صورت عددی معتبر (مثلاً 165) وارد کنید 🌷",
            delete_after=20,
        )
        return

    await state.update_data(height_cm=height)
    await state.set_state(RegistrationState.weight)
    await send_temp_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text="وزن خود را به کیلوگرم وارد کنید (مثلاً 70).",
        delete_after=90,
    )


@router.message(RegistrationState.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    try:
        weight = float((message.text or "").strip())
        if weight < 35 or weight > 200:
            raise ValueError()
    except ValueError:
        await send_temp_message(
            bot=message.bot,
            chat_id=message.chat.id,
            text="وزن را به صورت عددی معتبر (مثلاً 70) وارد کنید 🌸",
            delete_after=20,
        )
        return

    await state.update_data(weight_kg=weight)
    await state.set_state(RegistrationState.goal)
    await send_temp_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text="هدف اصلی شما چیست؟",
        reply_markup=goal_keyboard(),
        delete_after=90,
    )


@router.message(RegistrationState.goal)
async def process_goal(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    mapping = {
        "چربی‌سوزی": "weight_loss",
        "عضله‌سازی": "muscle_gain",
        "تناسب اندام": "maintenance",
    }
    if text not in mapping:
        await send_temp_message(
            bot=message.bot,
            chat_id=message.chat.id,
            text="لطفاً یکی از گزینه‌های پیشنهادی را انتخاب کنید 💚",
            delete_after=20,
        )
        return

    await state.update_data(goal=mapping[text])
    await state.set_state(RegistrationState.user_type)
    await send_temp_message(
        bot=message.bot,
        chat_id=message.chat.id,
        text="نوع عضویت شما چیست؟",
        reply_markup=user_type_keyboard(),
        delete_after=90,
    )


@router.message(RegistrationState.user_type)
async def process_user_type(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    mapping = {
        "عادی": "normal",
        "دانشجویی": "student",
        "کارمندی": "employee",
    }
    if text not in mapping:
        await send_temp_message(
            bot=message.bot,
            chat_id=message.chat.id,
            text="لطفاً فقط یکی از گزینه‌های عضویت را انتخاب کنید 🌟",
            delete_after=20,
        )
        return

    await state.update_data(user_type=mapping[text])
    data = await state.get_data()
    await state.clear()

    session = get_session()
    try:
        user = get_user_by_telegram_id(
            session=session,
            telegram_id=str(message.from_user.id),
        )
        if user is None:
            from app.services.subscriptions import create_user

            user = create_user(
                session=session,
                telegram_id=str(message.from_user.id),
                full_name=message.from_user.full_name,
            )

        update_user_profile(
            session=session,
            user=user,
            gender=data.get("gender"),
            age=data.get("age"),
            height_cm=data.get("height_cm"),
            weight_kg=data.get("weight_kg"),
            goal=data.get("goal"),
            user_type=data.get("user_type"),
        )
    finally:
        session.close()

    summary = (
        "پروفایل شما با موفقیت ذخیره شد ✅\n\n"
        "از این پس برنامه‌ها و اشتراک‌ها بر اساس اطلاعات شما تنظیم می‌شوند. 🌸"
    )
    await message.answer(summary)

