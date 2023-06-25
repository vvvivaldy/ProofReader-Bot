from handlers.D_paid_function_handlers import *
from callbacks.trader_callbacks import *

@dp.message_handler(Text(equals='Ключи'))
async def keys(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Выберите действие",
                           reply_markup=kb_keys)


@dp.message_handler(Text(equals='Вернуться'))
async def keys(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы вернулись в меню",
                           reply_markup=kb_trader)
    

@dp.message_handler(Text(equals='Статистика Профиля'))
async def prof_stat(message: types.Message):
    await bot.send_video(chat_id=message.from_user.id,
                           video='https://c.mql5.com/1/78/open-uri20150119-12-2b4861__1.gif',
                           caption='Статистика Профиля',
                           reply_markup=ikb_trader_stat)