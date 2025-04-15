from aiogram.fsm.state import StatesGroup, State


class TagsCreationStates(StatesGroup):
    title = State()
    icon = State()
