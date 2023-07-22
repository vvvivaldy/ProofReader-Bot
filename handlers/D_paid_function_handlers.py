from handlers.C_admin_panel_handlers  import *
from callbacks.paid_callbacks import *


# Хендлер Авторизации
@dp.message_handler(Text(equals="Авторизация"))
async def auth_func(message: types.Message):
    if paid_validate(message.from_user.id) or trader_validate(message.from_user.id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        if trader_validate(message.from_user.id):
            cursor.execute("SELECT status FROM traders WHERE trader_id = ?", (message.from_user.id,))
        else:
            cursor.execute("SELECT status FROM users WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        if result[0] == "paid" or result[0] == "trader":
            await bot.send_message(chat_id=message.from_user.id,
                                text="Введите ваш <b>api_key</b> и <b>api_secret</b> через пробел: ",
                                parse_mode="HTML")
            await Auth.api.set()
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                text="Вы еще не оплатили подписку",
                                parse_mode="HTML")
    else: 
        await bot.send_message(chat_id=message.from_user.id,
                           text="Мы не предусмотрели данный запрос. Повторите попытку.")


# Хендлер управления плечом
@dp.message_handler(Text(equals="Кредитное плечо"))
async def leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,    
                            text="Выберите действие:",
                            reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
    

@dp.message_handler(Text(equals="Максимальное плечо монеты"))
async def coin_info(message: types.Message, state: FSMContext) -> None:
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Выберите вид контракта -> Линейный/Обратный", reply_markup=kb_contract)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
            

@dp.message_handler(Text(equals="Линейный"))
async def contract_type(message: types.Message, state: FSMContext):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Введите аббревиатуру токена (пример -> BTCUSD)")
        await state.set_state(Leverage.leverage_linear)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Обратный"))
async def contract_type(message: types.Message, state: FSMContext):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Введите аббревиатуру токена (пример -> BTCUSD)")
        await state.set_state(Leverage.leverage_inverse)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Назад в меню плеча"))
async def back(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Вы вернулись в меню плеча", reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(state=Leverage.leverage_linear)
async def contract_type(message: types.Message, state: FSMContext):
    token = message.text
    session = HTTP(testnet=False)
    if paid_validate(message.from_user.id):
        try:
            info = session.get_risk_limit(
            category="linear",
            symbol=token,
            )
            symbol_info = info["result"]["list"][0]["symbol"]
            max_leverage = info["result"]["list"][0]["maxLeverage"]
            await bot.send_message(chat_id=message.from_user.id, text = f'''Токен -> <b>{symbol_info}</b>\nМаксимальное плечо -> <b>{max_leverage}</b>''', parse_mode="HTML", reply_markup=kb_leverage)
        except:
            await bot.send_message(chat_id=message.from_user.id, text = "Формат монеты неверен, попробуйте еще раз", reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                            text="Мы не предусмотрели данный запрос. Повторите попытку.")
    await state.finish()


@dp.message_handler(state=Leverage.leverage_inverse)
async def contract_type(message: types.Message, state: FSMContext):
    token = message.text
    session = HTTP(testnet=False)
    if paid_validate(message.from_user.id):
        try:
            info = session.get_risk_limit(
            category="inverse",
            symbol=token,
            )
            symbol_info = info["result"]["list"][0]["symbol"]
            max_leverage = info["result"]["list"][0]["maxLeverage"]
            await bot.send_message(chat_id=message.from_user.id, text = f'''Токен -> <b>{symbol_info}</b>\nМаксимальное плечо -> <b>{max_leverage}</b>''', parse_mode="HTML", reply_markup=kb_leverage)
        except:
            await bot.send_message(chat_id=message.from_user.id, text = "Формат монеты неверен, попробуйте еще раз", reply_markup=kb_leverage)
    else:
            await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
    await state.finish()


# Хендлер механизма подписки
@dp.message_handler(Text(equals="Подписка на трейдера"))
async def trader_keyy(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                            text = "Выберите действие",
                            reply_markup=kb_subscribe_on_trader)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
    

@dp.message_handler(Text(equals="Подписаться на трейдера"))
async def trader_key_subscribe(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Введите ключ трейдера")
        await TraderKey.trader_key_subscribe.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Отписаться от трейдера"))
async def trader_key_unsubscribe(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Вы уверены, что хотите отписаться?", reply_markup=kb_confirmation)
        await TraderKey.trader_key_unsubscribe.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Назад в меню подписки"))
async def back_menu_sub_trader(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Вы вернулись в меню подписки", reply_markup=kb_subscribe_on_trader)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(state=TraderKey.trader_key_unsubscribe)
async def trader_key_unsubscribe_confirmation(message: types.Message, state: FSMContext):
    if paid_validate(message.from_user.id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        confirmation = message.text
        if confirmation == "ДА":
            trader_id1 = cursor.execute(f"SELECT trader_sub_id FROM users WHERE user_id = {message.from_user.id}").fetchone()[0]
            if trader_id1 == "":
                await bot.send_message(chat_id=message.from_user.id, text="Вы не подписаны ни на одного трейдера", reply_markup=kb_subscribe_on_trader)
            else:
                try:
                    cursor.execute(f'UPDATE users SET trader_sub_id = "" WHERE user_id = {message.from_user.id}')
                    subs = cursor.execute(f"SELECT trader_subs FROM traders WHERE trader_id = '{trader_id1[0]}'").fetchone()[0]
                    subs = subs.split(" ")
                    for i in subs:
                        if i == str(message.from_user.id):
                            subs.remove(i)
                    new_subs = ' '.join(subs)     
                    cursor.execute(f"""UPDATE traders SET trader_subs = '{new_subs}' WHERE trader_id = '{trader_id1[0]}'""")
                    await bot.send_message(chat_id=message.from_user.id, text="Вы успешно отписались от трейдера!", reply_markup=kb_subscribe_on_trader)
                except:
                    await bot.send_message(chat_id=message.from_user.id, text="Вы не были подписаны на трейдера", reply_markup=kb_subscribe_on_trader)
                    await state.finish()   
                    return 
            
        else:
            await bot.send_message(chat_id=message.from_user.id, text="Изменения отменены", reply_markup=kb_subscribe_on_trader)

    conn.commit()
    cursor.close()
    await state.finish()

        
@dp.message_handler(state=TraderKey.trader_key_subscribe)
async def key_checker(message: types.Message, state: FSMContext):
    conn, cursor = db_connect()
    if message.text != "Назад":
        traders_keys = cursor.execute('SELECT key FROM trader_keys').fetchmany(100)
        key = message.text
        flag = False
        for i in traders_keys:
            if i[0] == key:
                trader_id1 = cursor.execute(f"SELECT trader_id FROM trader_keys WHERE key = '{key}'").fetchone()
                cursor.execute(f'UPDATE users SET trader_sub_id = "{trader_id1[0]}" WHERE user_id = {message.from_user.id}')
                subs = cursor.execute(f"SELECT trader_subs FROM traders WHERE trader_id = '{trader_id1[0]}'").fetchone()
                cursor.execute(f"""UPDATE traders SET trader_subs = '{subs[0]}' || ' ' || '{message.from_user.id}' WHERE trader_id = '{trader_id1[0]}'""")
                cursor.execute(f"""UPDATE trader_keys SET quantity = quantity + 1 WHERE key = '{key}'""")
                await bot.send_message(chat_id=message.from_user.id,
                               text = "Вы успешно подписались на трейдера!")
                flag = True

        if flag == False:
            await bot.send_message(chat_id=message.from_user.id,
                               text="Ключ введен неправильно, повторите попытку"
                               )
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню",
                               reply_markup=kb_reg)
        
        await state.finish()
        conn.commit()
        cursor.close()


# Хендлер получения Api
@dp.message_handler(state=Auth.api)
async def set_api(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['api'] = message.text
    s = await state.get_data()
    api_key = encrypt_api(s['api'].partition(' ')[0])
    api_secret = encrypt_api(s['api'].partition(' ')[2])
    try:
        test = HTTP(
            api_key=decrypt_api(api_key),
            api_secret=decrypt_api(api_secret))
        test.get_account_info()
    except:
        await bot.send_message(message.chat.id, 'Api key или Api secret указаны неверно. Повторите попытку', reply_markup=kb_unreg)
        await state.finish()
        return

    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    if not trader_validate(message.from_user.id):
        cursor.execute(f"""UPDATE users SET api_secret = "{api_secret}", api_key = "{api_key}"
                                WHERE user_id = {message.from_user.id}""")
        await bot.send_message(message.chat.id, 'Ваш профиль создан', reply_markup=kb_reg)

    else:
        cursor.execute(f"""UPDATE traders SET api_secret = "{api_secret}", api_key = "{api_key}"
                                        WHERE trader_id = {message.from_user.id}""")
        await bot.send_message(message.chat.id, 'Ваш профиль создан', reply_markup=kb_trader)
    conn.commit()
    cursor.close()
    await state.reset_state()
    await state.finish()


# Хендлер Профиля
@dp.message_handler(Text(equals="Профиль"))
async def profile_func(message: types.Message):
    if paid_validate(message.from_user.id):
        await message.answer(text="Выберите действие", reply_markup=kb_prof)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Подписка"))
async def balance_func(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        data = cursor.execute('SELECT subscribe_start, subscribe_finish, subscriptions FROM users WHERE user_id=?;',
                              (message.from_user.id,)).fetchone()
        a = ""
        match data[2]:
            case "week":
                a = SROKS[0]
            case "month":
                a = SROKS[1]
            case "3_month":
                a = SROKS[2]
            case "6_month":
                a = SROKS[3]
            case "year":
                a = SROKS[4]
        text = f"""<u>У вас активирована подписка на {a}</u>
<b>• Начало подписки:</b> {data[0]}
<b>• Конец подписки:</b> {data[1]}"""
        await bot.send_message(chat_id=message.from_user.id,
                         text=text,
                         parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


# Хендлер Баланса
@dp.message_handler(Text(equals="Баланс"))
async def balance_func(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        data = cursor.execute('SELECT api_secret, api_key FROM users WHERE user_id=?;', (message.from_user.id,)).fetchone()
        session = HTTP(
            api_key=decrypt_api(data[1]),
            api_secret=decrypt_api(data[0])
        )
        
        wallet_balance_data = session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]
        coins = wallet_balance_data["coin"]
        total_balance = wallet_balance_data["totalEquity"]
        total_balance_msg = ""

        for obj in coins:
            total_balance_msg += f"<b>{obj['coin']}</b>: <b>{obj['equity']}</b>\n"

        total_balance_msg += f"<b>Общий баланс: {total_balance}</b> $"
        await bot.send_message(chat_id=message.from_user.id,
                               text=total_balance_msg,
                               parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        

@dp.message_handler(Text(equals='Мои трейдеры'))
async def my_subs(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        subs = list(cursor.execute(f'SELECT trader_sub_id FROM users WHERE user_id = {message.from_user.id}').fetchone()[0].split())
        traders = 'Трейдеры,на которых вы подписаны: \n\n'
        if len(subs) > 0:
            for i in subs:
                info = cursor.execute(f'SELECT name FROM traders WHERE trader_id = {i} AND status = "trader"').fetchone()[0]
                traders += f'{info} \n'
        else:
            traders += 'Вы ни на кого не подписаны'
        await bot.send_message(chat_id=message.from_user.id,
                               text=traders,
                               reply_markup=kb_reg)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        

@dp.message_handler(Text(equals='Мои подписки'))
async def my_subs(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        subs = list(cursor.execute(f'SELECT trader_sub_id FROM users WHERE user_id = {message.from_user.id}').fetchone()[0].split())
        traders = '<b>Трейдеры,на которых вы подписаны: </b>\n\n'
        if len(subs) > 0:
            for i in subs:
                info = cursor.execute(f'SELECT name FROM traders WHERE trader_id = {i} AND status = "trader"').fetchone()[0]
                traders += f'{info} \n'
        else:
            traders += 'Увы, вы ни на кого не подписаны'
        await bot.send_message(chat_id=message.from_user.id,
                               text=traders,
                               parse_mode="HTML",
                               reply_markup=kb_reg)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")