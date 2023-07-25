from handlers.C_admin_panel_handlers import *
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
@dp.message_handler(Text(equals="Управление плечом"))
async def leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите действие:",
                               reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


# Хендлер профита и убытка
@dp.message_handler(Text(equals="Профит/убыток"))
async def profit_func(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Выберите период", reply_markup=kb_date)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Неделя"))
async def week(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        current_date = datetime.now().date()
        date_1_week_ago = current_date - timedelta(weeks=1)
        dates_date = []
        dates_total = []
        profit = 0
        dates = cursor.execute(f"""SELECT date_1 from orders WHERE user_id = '{message.from_user.id}'""").fetchall()
        for i in dates:
            date_object = datetime.strptime(i[0], '%Y-%m-%d').date()
            dates_date.append(date_object)
        for i in dates_date:
            if i >= date_1_week_ago:
                dates_total.append(i)
        for i in range(len(dates_total)):
            dates_total[i] = dates_total[i].strftime("%Y-%m-%d")
        for i in dates_total:
            profit_1 = cursor.execute(
                f"""SELECT profit FROM orders WHERE user_id = '{message.from_user.id}' AND date_1 = '{i}'""").fetchone()[
                0]
            profit_1 = int(profit_1)
            profit += profit_1
        if profit < 0:
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваш убыток составляет <b>{profit}$</b>",
                                   parse_mode="HTML")
        elif profit == 0:
            await bot.send_message(chat_id=message.from_user.id, text="Ваша прибыль составляет <b>0$</b>",
                                   parse_mode="HTML")
        else:
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваша прибыль составляет <b>{profit}$</b>",
                                   parse_mode="HTML")

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Месяц"))
async def week(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        current_date = datetime.now().date()
        one_month = date.today() + relativedelta(months=-1)
        dates_date = []
        dates_total = []
        profit = 0
        dates = cursor.execute(f"""SELECT date_1 from orders WHERE user_id = '{message.from_user.id}'""").fetchall()
        for i in dates:
            date_object = datetime.strptime(i[0], '%Y-%m-%d').date()
            dates_date.append(date_object)
        for i in dates_date:
            if i >= one_month:
                dates_total.append(i)
        for i in range(len(dates_total)):
            dates_total[i] = dates_total[i].strftime("%Y-%m-%d")
        for i in dates_total:
            profit_1 = cursor.execute(f"""SELECT profit FROM orders WHERE user_id = '{message.from_user.id}' AND 
            date_1 = '{i}'""").fetchone()[0]
            profit_1 = int(profit_1)
            profit += profit_1
        if profit < 0:
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваш убыток составляет <b>{profit}$</b>",
                                   parse_mode="HTML")
        elif profit == 0:
            await bot.send_message(chat_id=message.from_user.id, text="Ваша прибыль составляет <b>0$</b>",
                                   parse_mode="HTML")
        else:
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваша прибыль составляет <b>{profit}$</b>",
                                   parse_mode="HTML")

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Год"))
async def week(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        current_date = datetime.now().date()
        current_datee_str = current_date.strftime("%Y-%m-%d")
        cur = datetime.fromisoformat(current_datee_str)
        one_year = cur - relativedelta(years=1)
        dates_date = []
        dates_total = []
        profit = 0
        dates = cursor.execute(f"""SELECT date_1 from orders WHERE user_id = '{message.from_user.id}'""").fetchall()
        for i in dates:
            date_object = datetime.strptime(i[0], '%Y-%m-%d').date()
            dates_date.append(date_object)
        for i in dates_date:
            if i >= one_year.date():
                dates_total.append(i)
        for i in range(len(dates_total)):
            dates_total[i] = dates_total[i].strftime("%Y-%m-%d")
        for i in dates_total:
            profit_1 = cursor.execute(f"""SELECT profit FROM orders WHERE user_id = '{message.from_user.id}' 
            AND date_1 = '{i}'""").fetchone()[0]
            profit_1 = int(profit_1)
            profit += profit_1
        if profit < 0:
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваш убыток составляет <b>{profit}$</b>",
                                   parse_mode="HTML")
        elif profit == 0:
            await bot.send_message(chat_id=message.from_user.id, text="Ваша прибыль составляет <b>0$</b>",
                                   parse_mode="HTML")
        else:
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваша прибыль составляет <b>{profit}$</b>",
                                   parse_mode="HTML")

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Максимальное плечо монеты"))
async def coin_info(message: types.Message, state: FSMContext) -> None:
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Выберите вид контракта -> Линейный/Обратный",
                               reply_markup=kb_contract)
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


@dp.message_handler(Text(equals="Назад в статистику"))
async def back_statistics(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Вы вернулись в меню статистики", reply_markup=kb_stat)


@dp.message_handler(state=Leverage.leverage_linear)
async def contract_type(message: types.Message, state: FSMContext):
    token = message.text
    session = HTTP(testnet=False)
    if paid_validate(message.from_user.id):
        try:
            info_leverage = session.get_risk_limit(
                category="linear",
                symbol=token)
            symbol_info = info_leverage["result"]["list"][0]["symbol"]
            max_leverage = info_leverage["result"]["list"][0]["maxLeverage"]
            await bot.send_message(chat_id=message.from_user.id, text=f'''Токен -> <b>{symbol_info}</b>\nМаксимальное 
плечо -> <b>{max_leverage}</b>''', parse_mode="HTML", reply_markup=kb_leverage)
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Формат монеты неверен, попробуйте еще раз",
                                   reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
    await state.finish()


# Хендлер статистики
@dp.message_handler(Text(equals="Статистика"))
async def statistics(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Выберите действие", reply_markup=kb_stat)


@dp.message_handler(state=Leverage.leverage_inverse)
async def contract_type(message: types.Message, state: FSMContext):
    token = message.text
    session = HTTP(testnet=False)
    if paid_validate(message.from_user.id):
        try:
            info_l = session.get_risk_limit(
                category="inverse",
                symbol=token,
            )
            symbol_info = info_l["result"]["list"][0]["symbol"]
            max_leverage = info_l["result"]["list"][0]["maxLeverage"]
            await bot.send_message(chat_id=message.from_user.id, text=f'''Токен -> <b>{symbol_info}</b>\n
Максимальное плечо -> <b>{max_leverage}</b>''', parse_mode="HTML", reply_markup=kb_leverage)
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Формат монеты неверен, попробуйте еще раз",
                                   reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
    await state.finish()


# Хендлер механизма подписки
@dp.message_handler(Text(equals="Подписка на трейдера"))
async def trader_keyy(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите действие",
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
        await bot.send_message(chat_id=message.from_user.id, text="Вы уверены, что хотите отписаться?",
                               reply_markup=kb_confirmation)
        await TraderKey.trader_key_unsubscribe.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals="Назад в меню подписки"))
async def back_menu_sub_trader(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text="Вы вернулись в меню подписки",
                               reply_markup=kb_subscribe_on_trader)
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
            trader_id1 = cursor.execute(f"SELECT trader_sub_id FROM users WHERE "
                                        f"user_id = {message.from_user.id}").fetchone()[0]
            if trader_id1 == "":
                await bot.send_message(chat_id=message.from_user.id, text="Вы не подписаны ни на одного трейдера",
                                       reply_markup=kb_subscribe_on_trader)
            else:
                try:
                    cursor.execute(f'UPDATE users SET trader_sub_id = "" WHERE user_id = {message.from_user.id}')
                    subs = cursor.execute(f"SELECT trader_subs FROM "
                                          f"traders WHERE trader_id = '{trader_id1}'").fetchone()[0]
                    subs = subs.split(" ")
                    for i in subs:
                        if i == str(message.from_user.id):
                            subs.remove(i)
                    new_subs = ' '.join(subs)
                    cursor.execute(
                        f"""UPDATE traders SET trader_subs = '{new_subs}' WHERE trader_id = '{trader_id1}'""")
                    await bot.send_message(chat_id=message.from_user.id, text="Вы успешно отписались от трейдера!",
                                           reply_markup=kb_subscribe_on_trader)
                except Exception as e:
                    await bot.send_message(chat_id=message.from_user.id, text="Вы не были подписаны на трейдера",
                                           reply_markup=kb_subscribe_on_trader)
                    await state.finish()
                    return

        else:
            await bot.send_message(chat_id=message.from_user.id, text="Изменения отменены",
                                   reply_markup=kb_subscribe_on_trader)

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
                trader_id1 = cursor.execute(f"SELECT trader_id FROM trader_keys WHERE key = '{key}'").fetchone()[0]
                cursor.execute(
                    f'UPDATE users SET trader_sub_id = "{trader_id1}" WHERE user_id = {message.from_user.id}')
                subs = cursor.execute(f"SELECT trader_subs FROM traders WHERE trader_id = '{trader_id1}'").fetchone()
                cursor.execute(f"""UPDATE traders SET trader_subs = '{subs[0]}' || ' ' || '{message.from_user.id}' 
WHERE trader_id = '{trader_id1}'""")
                cursor.execute(f"""UPDATE trader_keys SET quantity_tek = quantity_tek + 1 WHERE key = '{key}'""")
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вы успешно подписались на трейдера!", reply_markup=kb_reg)
                flag = True

        if not flag:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Ключ введен неправильно, повторите попытку"
                                   )
            conn.commit()
            cursor.close()
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
        await bot.send_message(message.chat.id, 'Api key или Api secret указаны неверно. Повторите попытку',
                               reply_markup=kb_unreg)
        await state.finish()
        return

    conn, cursor = db_connect()
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


@dp.message_handler(Text(equals="Настройки бота"))
async def profile_func(message: types.Message):
    if paid_validate(message.from_user.id):
        await message.answer(text="Выберите действие", reply_markup=kb_settings)
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


# Хендлеры открытых сделок
@dp.message_handler(Text(equals="Открытые сделки"))
async def open_orders(message: types.Message):
    conn, cursor = db_connect()
    data = cursor.execute(
        f"""SELECT order_id, tp_order_id, sl_order_id, trade_pair, take_profit, stop_loss, trader_id, status, 
        open_price, close_price, close_order_id, profit, qty FROM orders 
        WHERE user_id = '{message.from_user.id}'""").fetchall()
    res = ''
    if data[0][7] == "open":
        for item in data:
            res += f"""
Базовый ордер: {item[0]}
TP ордер: {item[1]}
SL ордер: {item[2]}
Валютная пара: {item[3]}
Уровень TakeProfit: {item[4]}
Уровень StopLoss: {item[5]}
Уровень открытия базового ордера: {item[8]}
Кол-во монет: {item[12]}
----------------------
"""
    if res != '':
        await bot.send_message(chat_id=message.from_user.id,
                               text=res,
                               reply_markup=kb_stat)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='У вас нет открытых ордеров, которые были отслежены при помощи ProofReader.',
                               reply_markup=kb_stat)
    return


# Хендлер Баланса
@dp.message_handler(Text(equals="Баланс"))
async def balance_func(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        data = cursor.execute('SELECT api_secret, api_key FROM users WHERE user_id=?;',
                              (message.from_user.id,)).fetchone()
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

        total_balance_msg += f"\n<b>Общий баланс: {total_balance}</b> $"
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
        subs = list(
            cursor.execute(f'SELECT trader_sub_id FROM users WHERE user_id = {message.from_user.id}').fetchone()[
                0].split())
        traders = '<b>Трейдеры,на которых вы подписаны:</b> \n\n'
        if len(subs) > 0:
            for i in subs:
                info = \
                    cursor.execute(f'SELECT name FROM traders WHERE trader_id = {i} AND status = "trader"').fetchone()[
                        0]
                traders += f'• {info} \n'
        else:
            traders += 'Вы ни на кого не подписаны'
        await bot.send_message(chat_id=message.from_user.id,
                               text=traders,
                               reply_markup=kb_reg, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Мои подписки'))
async def my_subs(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        subs = list(
            cursor.execute(f'SELECT trader_sub_id FROM users WHERE user_id = {message.from_user.id}').fetchone()[
                0].split())
        traders = '<b>Трейдеры,на которых вы подписаны: </b>\n\n'
        if len(subs) > 0:
            for i in subs:
                info = cursor.execute(f'SELECT name FROM traders WHERE trader_id = {i} '
                                      f'AND status = "trader"').fetchone()[0]
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


@dp.message_handler(Text(equals='Установить плечо'))
async def take_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        leverage = cursor.execute(f'SELECT leverage FROM users WHERE user_id = {message.from_user.id}').fetchone()[0]
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваше текущее плечо: X{leverage} . По дефолту X1',
                               reply_markup=kb_set_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Изменить'))
async def edit_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'(Мы не рекомендуем ставить слишком большое плечо на время бета-тестирования. '
                                    f'Оптимально будет до Х15)\n\nВведите размер плеча в виде одного числа:')
        await Set_Leverage.leverage.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(state=Set_Leverage.leverage)
async def set_leverage(message: types.Message, state=FSMContext):
    async with state.proxy() as proxy:
        proxy['leverage'] = message.text
    leverage = await state.get_data()
    conn, cursor = db_connect()
    if message.text.isdigit() and (0 < int(message.text) <= 100):
        cursor.execute(f'UPDATE users SET leverage = {int(message.text)} WHERE user_id = {message.from_user.id}')
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Теперь Ваше плечо: X{leverage["leverage"]} . По дефолту X1',
                               reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Плечо слишком большое либо введено некорректно.',
                               reply_markup=kb_set_leverage)
    conn.commit()
    cursor.close()
    await state.finish()


@dp.message_handler(Text(equals='Настройки бота'))
async def settings(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_photo(chat_id=message.from_user.id,
                             photo='https://wallpapers.com/images/hd/cool-neon-blue-lf1zlxnvobv5cn1r.jpg',
                             caption='Настройки бота',
                             reply_markup=kb_settings)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Управление плечом'))
async def control_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_photo(chat_id=message.from_user.id,
                             photo='https://i.pinimg.com/originals/c2/9a/12/c29a120f645acc23afb709366c06b0bb.jpg',
                             caption='Настройте с помощью клавиатуры',
                             reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Сбросить плечо'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        cursor.execute(f'UPDATE users SET leverage = 1 WHERE user_id = {message.from_user.id}')
        conn.commit()
        cursor.close()
        await bot.send_message(chat_id=message.from_user.id,
                               text='Плечо сброшено. \nТеперь ваше плечо является X1 (по дефолту).',
                               reply_markup=kb_leverage)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Сумма сделки'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите вариант, благодаря котрому будет расчитываться сумма каждой сделки.",
                               reply_markup=kb_summ)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Процент от депозита'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Напишите процент от депозита одним числом.\n<b"
                                    ">Мы не советуем тратить на одну сделку более 50 %.</b>",
                               parse_mode="HTML")
        await Set_Percent.percent.set()

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(state=Set_Percent.percent)
async def set_leverage(message: types.Message, state=FSMContext):
    async with state.proxy() as proxy:
        proxy['percent'] = message.text
    percent = await state.get_data()
    percent = percent["percent"]
    if percent != "Назад в настройки":
        try:
            if 0 < int(percent) <= 100:
                conn, cursor = db_connect()
                cursor.execute(f"""UPDATE users SET sum = "{percent} %" WHERE user_id = {message.from_user.id}""")
                conn.commit()
                cursor.close()
                await bot.send_message(message.chat.id,
                                       f'Изменения были успешно сохранены, теперь на каждую сделку будет тратиться<b> '
                                       f'{percent} %</b> от депозита.',
                                       parse_mode="HTML",
                                       reply_markup=kb_settings)
                await state.reset_state()
                await state.finish()
            else:
                await bot.send_message(message.chat.id,
                                       f'Вы указали недопустимое число. Повторите попытку.')

        except ValueError:
            await bot.send_message(message.chat.id,
                                   f'Вы должны написать только число. Повторите попытку.')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в настройки бота",
                               reply_markup=kb_settings)
        await state.reset_state()
        await state.finish()


@dp.message_handler(Text(equals='Фиксированная сумма'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Напишите сумму (в долларах), которая будет тратиться на сделку целым числом.\n"
                                    "<b>Мы не советуем тратить на одну сделку более 50 % от депозита.</b>",
                               parse_mode="HTML")
        await Set_Dollars.dollars.set()

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(state=Set_Dollars.dollars)
async def set_leverage(message: types.Message, state=FSMContext):
    async with state.proxy() as proxy:
        proxy['dollars'] = message.text
    dollars = await state.get_data()
    dollars = dollars["dollars"]
    if dollars != "Назад в настройки":
        try:
            conn, cursor = db_connect()
            data = cursor.execute('SELECT api_secret, api_key FROM users WHERE user_id=?;',
                                  (message.from_user.id,)).fetchone()
            session = HTTP(
                api_key=decrypt_api(data[1]),
                api_secret=decrypt_api(data[0])
            )

            wallet_balance_data = session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]
            total_balance = wallet_balance_data["totalEquity"]
            print(total_balance)
            if 0 < int(dollars) <= float(total_balance):
                conn, cursor = db_connect()
                cursor.execute(f"""UPDATE users SET sum = "{dollars} $" WHERE user_id = {message.from_user.id}""")
                conn.commit()
                cursor.close()
                await bot.send_message(message.chat.id,
                                       f'Изменения были успешно сохранены, теперь на каждую сделку будет тратиться<b> '
                                       f'{dollars} $</b> от депозита.',
                                       parse_mode="HTML",
                                       reply_markup=kb_settings)
                await state.reset_state()
                await state.finish()
            else:
                await bot.send_message(message.chat.id,
                                       f'Вы указали недопустимое число, или на вашем деривативном счету '
                                       f'не достаточно средств. Повторите попытку.')

        except ValueError:
            await bot.send_message(message.chat.id,
                                   f'Вы должны написать только число. Повторите попытку.')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в настройки бота.",
                               reply_markup=kb_settings)
        await state.reset_state()
        await state.finish()


@dp.message_handler(Text(equals='Назад в настройки'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в настройки бота.",
                               reply_markup=kb_settings)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Назад в профиль'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в профиль.",
                               reply_markup=kb_prof)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Назад в меню информации'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню информации.",
                               reply_markup=kb_inform)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='О нас'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text=DESCR, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Остановить работу'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        data = cursor.execute(f"SELECT flag FROM users WHERE user_id = {message.from_user.id}").fetchone()
        if data[0] == "true":
            cursor.execute(f"UPDATE users SET flag = 'false' WHERE user_id = {message.from_user.id}")
            await bot.send_message(chat_id=message.from_user.id,
                                   text="<b>ProofReader прекратил отслеживание❌</b> Нажмите на кнопку \"Запустить"
                                        " ProofReader\", чтобы бот снова начал получать ордера профессионального"
                                        " трейдера.",
                                   parse_mode="HTML",
                                   reply_markup=kb_reg)
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="ProofReader не запущен.",
                                   parse_mode="HTML",
                                   reply_markup=kb_reg)
        conn.commit()
        cursor.close()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Запустить ProofReader'))
async def drop_leverage(message: types.Message):
    if paid_validate(message.from_user.id):
        conn, cursor = db_connect()
        data = cursor.execute(
            f"SELECT sum, flag, trader_sub_id, leverage FROM users WHERE user_id = {message.from_user.id}").fetchone()
        if data[0] != "" and data[1] == "false" and data[2] != "":
            cursor.execute(f"UPDATE users SET flag = 'true' WHERE user_id = {message.from_user.id}")
            if "$" in data[0]:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="<b>Вы запустили Proofreader✅</b> Теперь все сделки, которые "
                                            "совершает трейдер, "
                                            f"будут отоброжаться и у вас!\n\n<b>Цена одной сделки:</b> <u>{data[0]}</u>"
                                            f"\n"
                                            f"<b>Плечо, используемое для каждого ордера:</b> <u>{data[3]} x</u>",
                                       parse_mode="HTML", reply_markup=kb_reg_work)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"<b>Вы запустили Proofreader✅</b> Теперь все сделки, которые "
                                            f"совершает трейдер, "
                                            f"будут отоброжаться и у вас!\n\n<b>Цена одной сделки:</b> <u>{data[0]} "
                                            f"от депозита</u>\n"
                                            f"<b>Плечо, используемое для каждого ордера:</b> <u>{data[3]} x</u>",
                                       parse_mode="HTML", reply_markup=kb_reg_work)
            conn.commit()
            cursor.close()
        else:
            text = ""
            if "$" not in data[0] and "%" not in data[0]:
                text += "• Вы не указали сумму сделки. Сделайте это в настройках бота.\n"
            if data[1] != "false":
                text += "• ProofReader уже работает. Напишите \"Остановить работу\", если хотите приостановить бота.\n"
            if len(data[2]) == 0:
                text += "• Вы не подписаны ни на одного трейдера. " \
                        "Сделайте это, нажав на кнопку \"Подписка на трейдера\"."
            await bot.send_message(chat_id=message.from_user.id,
                                   text=text,
                                   parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
