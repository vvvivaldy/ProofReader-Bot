from aiogram.dispatcher.filters.state import StatesGroup, State
from asyncio import gather, run

class Auth(StatesGroup):
    api = State()


class Bl_Id_Trader(StatesGroup):
    id = State()


class Bl_Id_User(StatesGroup):
    id = State()


class UserDel(StatesGroup):
    id = State()

class UserStatus(StatesGroup):
    status = State()

class TraderStatus(StatesGroup):
    status = State()

class SetUserSubscriptionStatus(StatesGroup):
    sub_status = State()

class EditApi(StatesGroup):
    api = State()

class EditApiTrader(StatesGroup):
    api = State()

class Key_Duration(StatesGroup):
    date = State()


class Activation_Quantity(StatesGroup):
    quantity = State()


class Key_Delete(StatesGroup):
    key = State()

