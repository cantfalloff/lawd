from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    name = State()
    password = State()
