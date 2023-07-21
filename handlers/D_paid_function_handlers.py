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
                            text = "Выберите действие:",
                            reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
    

@dp.message_handler(Text(equals="Информация о плече монеты"))
async def coin_info(message: types.Message, state: FSMContext) -> None:
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Введите Аббревиатуру Leveraged Token (пример -> BTC3L или BTC3S)")
        await state.set_state(Leverage.leverage_1)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Введите Аббревиатуру Leveraged Token (пример -> BTC3L или BTC3S)")
        await state.set_state(Leverage.leverage_1)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        

@dp.message_handler(state=Leverage.leverage_1)
async def coin_leverage(message: types.Message, state: FSMContext):
    coin = message.text
    session = HTTP(testnet=True)
    try: 
        info = session.get_leveraged_token_info(
        ltCoin=coin)
        fundFee = str(info["result"]["list"][0]["fundFee"]) + " -> Ежедневная плата за пользование плечом"
        ltStatus = str(info["result"]["list"][0]["ltStatus"]) + " -> Статус (подробнее https://bybit-exchange.github.io/docs/v5/enum#ltstatus)"
        maxPurchase = str(info["result"]["list"][0]["maxPurchase"]) + " -> Максимальная сумма для единоразовой покупки"
        minPurchase = str(info["result"]["list"][0]["minPurchase"]) + " -> Минимальная сумма для единоразовой покупки"
        maxRedeem = str(info["result"]["list"][0]["maxRedeem"]) + " -> Максиммальное количество для единоразового выкупа"
        minRedeem = str(info["result"]["list"][0]["minRedeem"]) + " -> Минимальное количество для единоразового выкупа"
        maxRedeemDaily = str(info["result"]["list"][0]["maxRedeemDaily"]) + " -> Максимальное количество для выкупа за один день"
        purchaseFeeRate = str(info["result"]["list"][0]["purchaseFeeRate"]) + " -> Ставка платы за покупку"
        redeemFeeRate = str(info["result"]["list"][0]["redeemFeeRate"]) + " -> ???"
        manageFeeRate = str(info["result"]["list"][0]["manageFeeRate"]) + " -> Ставка платы за Менджмент"
        value = str(info["result"]["list"][0]["value"]) + " -> Номинальная стоимость активов"

        await bot.send_message(chat_id=message.from_user.id, text = f'''{fundFee}\n\n{ltStatus}\n\n{maxPurchase}
        \n{minPurchase}
        \n{maxRedeem}
        \n{minRedeem}
        \n{maxRedeemDaily}
        \n{purchaseFeeRate}
        \n{manageFeeRate}
        \n{value}''')
    except:
        await bot.send_message(chat_id=message.from_user.id, text = "Формат монеты неверен, попробуйте еще раз", reply_markup=kb_leverage)

    await state.finish()


# Хендлер механизма подписки
@dp.message_handler(Text(equals="Подписка на трейдера"))
async def trader_keyy(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text = "Выберите действие",
                        reply_markup=kb_subscribe_on_trader)
@dp.message_handler(Text(equals="Подписаться на трейдера"))
async def trader_key_subscribe(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text="Введите ключ трейдера")
    await state.set_state(TraderKey.trader_key_subscribe)

@dp.message_handler(Text(equals="Отписаться от трейдера"))
async def trader_key_unsubscribe(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text="Вы уверены, что хотите отписаться?", reply_markup=kb_confirmation)
    await state.set_state(TraderKey.trader_key_unsubscribe)

@dp.message_handler(Text(equals="Назад в меню подписки"))
async def back_menu_sub_trader(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Вы вернулись в меню подписки", reply_markup=kb_subscribe_on_trader)

@dp.message_handler(state=TraderKey.trader_key_unsubscribe)
async def trader_key_unsubscribe_confirmation(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    confirmation = message.text
    if confirmation == "ДА":
        trader_id1 = cursor.execute(f"SELECT trader_sub_id FROM users WHERE user_id = {message.from_user.id}").fetchone()
        if trader_id1 == "o":
            await bot.send_message(chat_id=message.from_user.id, text="Вы не подписаны ни на одного трейдера", reply_markup=kb_subscribe_on_trader)
        else:
            cursor.execute(f'UPDATE users SET trader_sub_id = "none" WHERE user_id = {message.from_user.id}')
            try:
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
            
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Изменения отменены", reply_markup=kb_subscribe_on_trader)

    conn.commit()
    cursor.close()
    await state.finish()

@dp.message_handler(state=TraderKey.trader_key_subscribe)
@dp.message_handler(Text(equals="Ввести ключ трейдера"))
async def trader_keyy(message: types.Message, state: FSMContext) -> None:
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                            text = "Введите <b>ключ трейдера</b>",
                            parse_mode="HTML")
        await state.set_state(TraderKey.trader_key)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        
    
@dp.message_handler(state=TraderKey.trader_key)
async def key_checker(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
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
                           text = "Вы успешно подписались на трейдера!"
                           )
            flag = True
            
    if flag == False:
        await bot.send_message(chat_id=message.from_user.id,
                           text = "Ключ введен неправильно, повторите попытку"
                           )
        
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
        await message.answer(text="Выберите действие", reply_markup=kb_profile)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


# Хендлер Баланса
@dp.message_handler(Text(equals="Баланс"))
async def balance_func(message: types.Message):
    if paid_validate(message.from_user.id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
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
        

@dp.message_handler(Text(equals='Мои подписки'))
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
            traders += 'Увы, вы ни на кого не подписаны'
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
        traders = 'Трейдеры,на которых вы подписаны: \n\n'
        if len(subs) > 0:
            for i in subs:
                info = cursor.execute(f'SELECT name FROM traders WHERE trader_id = {i} AND status = "trader"').fetchone()[0]
                traders += f'{info} \n'
        else:
            traders += 'Увы, вы ни на кого не подписаны'
        await bot.send_message(chat_id=message.from_user.id,
                               text=traders,
                               reply_markup=kb_reg)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")