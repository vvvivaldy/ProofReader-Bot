from aiogram.dispatcher.filters.state import StatesGroup, State


class Auth(StatesGroup):
    api = State()


class Bl_Id_Trader(StatesGroup):
    id = State()


class Bl_Id_User(StatesGroup):
    id = State()


class UserDel(StatesGroup):
    id = State()