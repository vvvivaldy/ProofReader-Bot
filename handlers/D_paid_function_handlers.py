from handlers.C_admin_panel_handlers  import *
from callbacks.paid_callbacks import *


# Хендлер Авторизации
@dp.message_handler(Text(equals="Авторизация"))
async def auth_func(message: types.Message):
    if paid_validate(message.from_user.id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        if result[0] == "paid":
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

# Хендлер механизма подписки
@dp.message_handler(Text(equals="Ввести ключ трейдера"))
async def trader_keyy(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text = "Введите <b>ключ трейдера</b>",
                           parse_mode="HTML")
    await state.set_state(TraderKey.trader_key)
    
@dp.message_handler(state=TraderKey.trader_key)
async def key_checker(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    traders_keys = cursor.execute('SELECT key FROM trader_keys').fetchmany(100)
    key = message.text
    flag = False
    for i in traders_keys:
        if i[0] == key:
            trader_id = cursor.execute(f"SELECT trader_id FROM trader_keys WHERE key = '{key}'").fetchone()
            cursor.execute(f'UPDATE users SET trader_sub_id = "{trader_id[0]}" WHERE user_id = {message.from_user.id}')
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
        await state.finish()
    s = await state.get_data()
    api_key = encrypt_api(s['api'].partition(' ')[0])
    api_secret = encrypt_api(s['api'].partition(' ')[2])
    try:
        test = HTTP(
            api_key=decrypt_api(api_key),
            api_secret=decrypt_api(api_secret))
        test.get_account_info()
    except exceptions.InvalidRequestError as e:
        await bot.send_message(message.chat.id, 'Api key или Api secret указаны неверно. Повторите попытку', reply_markup=kb_unreg)
        print(e)
        return
    
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE users SET api_secret = "{api_secret}", api_key = "{api_key}"
                            WHERE user_id = {message.from_user.id}""")
    conn.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Ваш профиль создан', reply_markup=kb_reg)



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
            api_key=decrypt_api(data[1][2:-1]),
            api_secret=decrypt_api(data[0][2:-1])
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