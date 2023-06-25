from handlers.D_paid_function_handlers import *


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
