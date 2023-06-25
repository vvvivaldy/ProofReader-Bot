from handlers.A_head_of_handlers import *


@dp.callback_query_handler(lambda e: e.data[0] == 'E')
async def trader_callbacks(callback: types.CallbackQuery,):
    callback.data = callback.data[1:]
    match callback.data:
        # Бесконечное колво активаций
        case 'infinity':
            conn, cursor = db_connect()
            with open('cache/keys.txt', 'r') as file:
                key = file.readline()
            cursor.execute(f"UPDATE trader_keys SET quantity = 999999 WHERE key = '{key}';")
            conn.commit()
            cursor.close()
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Напишите дату, до которой будет работать ключ в формате хх-хх-хххх или напишите '<b>Бессрочно</b>', чтобы ключ работал всегда.",
                                   parse_mode="HTML")
            await Key_Duration.date.set()
        case 'personal':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Напишите возможное количество активаций. <b>Как только количество активаций будет исчерпано - ключ удалится</b>.",
                                   parse_mode="HTML")
            await Activation_Quantity.quantity.set()


# Количество активаций
@dp.message_handler(state=Activation_Quantity.quantity)
async def check_trader_status(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['quantity'] = message.text
        await state.finish()
    s = await state.get_data()
    quantity = s["quantity"]
    conn, cursor = db_connect()
    with open('cache/keys.txt', 'r') as file:
        key = file.readline()
    cursor.execute(f"UPDATE trader_keys SET quantity = {int(quantity)} WHERE key = '{key}';")
    conn.commit()
    cursor.close()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Напишите дату, до которой будет работать ключ в формате хх-хх-хххх или напишите '<b>Бессрочно</b>', чтобы ключ работал всегда.",
                           parse_mode="HTML")
    await Key_Duration.date.set()


# Длительность жизни ключа
@dp.message_handler(state=Key_Duration.date)
async def check_trader_status(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['date'] = message.text
        await state.finish()
    s = await state.get_data()
    date = s["date"]
    conn, cursor = db_connect()
    print(date)
    with open('cache/keys.txt', 'r') as file:
        key = file.readline()
    cursor.execute(f"UPDATE trader_keys SET duration = '{date}' WHERE key = '{key}';")
    conn.commit()
    cursor.close()
    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Ключ успешно добавлен!</b> Отправьте его пользователям, чтобы они смогли отслеживать ваши действия.",
                           parse_mode="HTML",
                           reply_markup=kb_trader)