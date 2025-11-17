from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    goal = State()
    user_type = State()

