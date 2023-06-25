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


@dp.message_handler(Text(equals='Создать ключ'))
async def new_key(message: types.Message):
    if trader_validate(message.from_user.id):
        letters = string.ascii_lowercase
        key = ''.join(random.choice(letters) for i in range(8))

        with open('cache/keys.txt', 'w') as file:
            file.write(key)

        conn, cursor = db_connect()
        cursor.execute(f"INSERT INTO trader_keys (trader_id, key) VALUES ('{message.from_user.id}', '{key}');")
        conn.commit()
        cursor.close()

        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите количество активаций.",
                               reply_markup=ikb_quantity)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
