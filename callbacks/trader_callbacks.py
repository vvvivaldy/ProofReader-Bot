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
                                   text="Напишите дату, до которой будет работать ключ в формате дд-мм-гггг или напишите '<b>Бессрочно</b>', чтобы ключ работал всегда.",
                                   parse_mode="HTML")
            await Key_Duration.date.set()
        case 'personal':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Напишите возможное количество активаций. <b>Как только количество активаций будет исчерпано - ключ удалится</b>.",
                                   parse_mode="HTML")
            await Activation_Quantity.quantity.set()

        case 'people':
            conn, cursor = db_connect()
            count = cursor.execute(f'SELECT count(*) FROM users WHERE subscriptions LIKE "{"%"+str(callback.from_user.id)+"%"}"').fetchone()[0]
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f'Кол-во ваших подписчиков: {count}')
        case 'OpenOrders':
            conn, cursor = db_connect()
            orders = cursor.execute(f'SELECT order_id, tp_order_id, sl_order_id, trade_pair, take_profit, stop_loss, open_price, qty FROM orders WHERE trader_id = {callback.from_user.id} AND status = "open"').fetchall()
            res = ''
            kb_trader = true_kb(callback.from_user.id)
            for item in orders:
                res+=f"""
Базовый ордер: {item[0]}
TP ордер: {item[1]}
SL ордер: {item[2]}
Валютная пара: {item[3]}
Уровень TP: {item[4]}
Уровень SL: {item[5]}
Уровень открытия базового ордера: {item[6]}
Кол-во монет: {item[7]}
----------------------
"""
            if res != '':
                await bot.send_message(chat_id=callback.from_user.id,
                                    text=res,
                                    reply_markup=kb_trader)
            else:
                await bot.send_message(chat_id=callback.from_user.id,
                                    text='У вас нет открытых ордеров,которые были отслежены',
                                    reply_markup=kb_trader)
            return
        
        case 'HistoryOrders':
            kb_trader = true_kb(callback.from_user.id)
            conn, cursor = db_connect()
            orders = cursor.execute(f'SELECT * FROM orders WHERE trader_id = {callback.from_user.id} AND status = "close"').fetchall()
            if len(orders) > 10:
                orders = orders[-11:]
            res = ''
            for item in orders:
                res+=f"""
Базовый ордер: {item[0]}
TP ордер: {item[1]}
SL ордер: {item[2]}
Валютная пара: {item[3]}
Уровень TP: {item[4]}
Уровень SL: {item[5]}
Уровень открытия базового ордера: {item[9]}
Уровень закрытия ордера: {item[10]}
Ордер закрытия: {item[11]}
Профит от сделки: {item[12]}
Кол-во монет: {item[13]}
----------------------
"""
            if res != '':
                await bot.send_message(chat_id=callback.from_user.id,
                                    text=res,
                                    reply_markup=kb_trader)
            else:
                await bot.send_message(chat_id=callback.from_user.id,
                                    text='У вас еще не было сделок, которые были отслежены.',
                                    reply_markup=kb_trader)
            return

        case 'pushOrder':
            kb_trader = true_kb(callback.from_user.id, mode = True)
            global stream_websockets
            tmp = stream_websockets[f'stream_{callback.from_user.id}'][1]
            tmp.create_order_in_object(tmp.ord, tmp.value, mode = True)
            await callback.message.edit_text(text='У ваших подписчиков в данный момент есть открытый вами ордер на данной валютной паре. Вероятно, Вы хотите докупить и/или изменить стоп-ордера. Вы хотите отправить им ТОЛЬКО ЧТО СОЗДАННЫЙ ВАМИ ордер, или не будете?\n\n\n ВЫ ОТПРАВИЛИ ОРДЕР✅')
            
            await bot.send_message(chat_id=callback.from_user.id, 
                                   text='Отслеживание OFF❌',
                                   reply_markup=kb_trader)

        case 'cancelOrder':
            kb_trader = true_kb(callback.from_user.id, mode=True)
            await callback.message.edit_text(text='У ваших подписчиков в данный момент есть открытый вами ордер на данной валютной паре. Вероятно, Вы хотите докупить и/или изменить стоп-ордера. Вы хотите отправить им ТОЛЬКО ЧТО СОЗДАННЫЙ ВАМИ ордер, или не будете?\n\n\n ВЫ ОТМЕНИЛИ ОТПРАВКУ ОРДЕРА💥')
            await bot.send_message(chat_id=callback.from_user.id, text='Отслеживание OFF❌', reply_markup=kb_trader)


# Удаление ключей
@dp.message_handler(state=Key_Delete.key)
async def key_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['key'] = message.text
    s = await state.get_data()
    key = s["key"]
    conn, cursor = db_connect()
    valid = cursor.execute(f"SELECT trader_id FROM trader_keys WHERE key = '{key}'").fetchone()
    kb_trader = true_kb(message.from_user.id)
    if valid is not None:
        cursor.execute(f"DELETE FROM trader_keys WHERE key = '{key}'")
        conn.commit()
        cursor.close()
        await bot.send_message(chat_id=message.from_user.id,
                               text="Ключ был удален. Люди, которые использовали его, больше не смогут отследивать ваши действия",
                               reply_markup=kb_trader)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Такого ключа не существует. Повторите попытку",
                               reply_markup=kb_trader)
    await state.reset_state()


# Количество активаций
@dp.message_handler(state=Activation_Quantity.quantity)
async def activation_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['quantity'] = message.text
    s = await state.get_data()
    quantity = s["quantity"]
    conn, cursor = db_connect()
    kb_trader = true_kb(message.from_user.id)
    with open('cache/keys.txt', 'r') as file:
        key = file.readline()
    try:
        cursor.execute(f"UPDATE trader_keys SET quantity = {int(quantity)} WHERE key = '{key}';")
        conn.commit()
        cursor.close()
        await bot.send_message(chat_id=message.from_user.id,
                               text="Напишите дату, до которой будет работать ключ в формате дд-мм-гггг или напишите '<b>Бессрочно</b>', чтобы ключ работал всегда.",
                               parse_mode="HTML")
        await state.reset_state()
        await Key_Duration.date.set()
    except ValueError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы должны ввести кол-во активаций одним числом. Повторите попытку",
                               reply_markup=kb_trader)
        cursor.execute(f"DELETE FROM trader_keys WHERE key = '{key}'")
        conn.commit()
        cursor.close()
        await state.reset_state()


# Длительность жизни ключа
@dp.message_handler(state=Key_Duration.date)
async def key_duration(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['date'] = message.text
        await state.finish()
    s = await state.get_data()
    kb_trader = true_kb(message.from_user.id)
    date = s["date"]
    conn, cursor = db_connect()
    with open('cache/keys.txt', 'r') as file:
        key = file.readline()
    try:
        if date.title() != "Бессрочно":
            a = datetime.strptime(date, '%d-%m-%Y').date()
            if a >= datetime.now().date():
                cursor.execute(f"UPDATE trader_keys SET duration = '{date}' WHERE key = '{key}';")
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Ваш ключ: <b>{key}</b> ! Отправьте его пользователям, чтобы они смогли отслеживать ваши действия.",
                                       parse_mode="HTML",
                                       reply_markup=kb_trader)
            else:
                cursor.execute(f"DELETE FROM trader_keys WHERE key = '{key}'")
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Вы ввели некорректную дату. Повторите попытку",
                                       parse_mode="HTML",
                                       reply_markup=kb_trader)
        else:
            cursor.execute(f"UPDATE trader_keys SET duration = '{date.title()}' WHERE key = '{key}';")
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Ваш ключ: <b>{key}</b> ! Отправьте его пользователям, чтобы они смогли отслеживать ваши действия.",
                                   parse_mode="HTML",
                                   reply_markup=kb_trader)
        conn.commit()
        cursor.close()
        await state.reset_state()

    except ValueError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы ввели дату в неправильным формате. Повторите попытку",
                               parse_mode="HTML",
                               reply_markup=kb_trader)
        cursor.execute(f"DELETE FROM trader_keys WHERE key = '{key}'")
        conn.commit()
        cursor.close()
        await state.reset_state()


