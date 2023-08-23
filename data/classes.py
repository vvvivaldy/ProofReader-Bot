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


class TraderKey(StatesGroup):
    trader_key_subscribe = State()
    trader_key_unsubscribe = State()
    

class SetUserSubscriptionStatus(StatesGroup):
    sub_status = State()


class EditApi(StatesGroup):
    api = State()
    

class Leverage(StatesGroup):
    leverage_linear = State()
    leverage_inverse = State()


class EditApiTrader(StatesGroup):
    api = State()


class Key_Duration(StatesGroup):
    date = State()


class Activation_Quantity(StatesGroup):
    quantity = State()


class Key_Delete(StatesGroup):
    key = State()


class Set_Leverage(StatesGroup):
    leverage = State()


class Set_Percent(StatesGroup):
    percent = State()


class Set_Dollars(StatesGroup):
    dollars = State()


class Set_Sale(StatesGroup):
    pr = State()


class Set_Salary(StatesGroup):
    proc = State()


class Personal_Id(StatesGroup):
    id = State()


class Set_Sale_Personal(StatesGroup):
    pr = State()


class Set_Salary_Personal(StatesGroup):
    proc = State()