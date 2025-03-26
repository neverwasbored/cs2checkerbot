from aiogram.fsm.state import StatesGroup, State


class steam_state(StatesGroup):
    steam_id = State()
