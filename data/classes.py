from aiogram.dispatcher.filters.state import StatesGroup, State


class Auth(StatesGroup):
    api_key = State()
    api_secret = State()