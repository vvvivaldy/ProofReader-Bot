from data.imports import *

bot = Bot(TG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Дата конца подписки
def next_month(today):
    delta = timedelta(days=30)
    return today + delta


# Успещный запуск бота
async def on_startup(_):
    print("Я был запущен")


# Хендлер старта
@dp.message_handler(commands=["start"])
async def start_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Приветствую, {message.from_user.username}! ВСТАВИТЬ ВСТУПЛЕНИЕ. "
                                f"Подробнее ты можешь узнать нажав  "
                                f"на кнопку \"Описание\"",
                           reply_markup=kb_free)
    # Подключение к бд
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    info = cursor.execute('SELECT * FROM users WHERE user_id=?;', (message.from_user.id, )).fetchone()
    # Если нет в бд
    if info is None:
        cursor.execute(f"""INSERT INTO users VALUES ('{message.from_user.id}', '0', '0', 'free', '', '');""")
        conn.commit()
    # Если есть в бд
    else:
        cursor.execute("SELECT status FROM users WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        # Если статус бесплатный
        if result[0] == "free":
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Мы нашли вашу учетную запись в базе данных.",
                                   reply_markup=kb_free)
        # Если статус платный
        elif result[0] == "paid":
            cursor.execute("SELECT api_secret FROM users WHERE user_id = ?", (message.from_user.id,))
            profile = cursor.fetchone()
            if profile[0] is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Мы нашли вашу учетную запись в базе данных.",
                                       reply_markup=kb_unreg)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Мы нашли вашу учетную запись в базе данных.",
                                       reply_markup=kb_reg)

    await message.delete()


# Хендлер Описания
@dp.message_handler(Text(equals="Описание"))
async def descr_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=DESCR)


# Хендлер Инструкции
@dp.message_handler(Text(equals="Инструкция"))
async def descr_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=INSTRUCT,
                           parse_mode="HTML",
                           reply_markup=kb_instruct)


# Хендлер Покупки подписки
@dp.message_handler(Text(equals="Оформить подписку"))
async def buy(message: types.Message):
    if PAYMENTS_TOKEN.split(":")[1] == "TEST":
        await bot.send_message(message.chat.id,
                               "Тестовый платеж")
    await bot.send_invoice(message.chat.id,
                           title="Подписка на Taber Bot",
                           description="Активация подписки на 1 месяц",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://i.postimg.cc/3RXYBqbV/kandinsky-download-1681585603018.png",
                           photo_width=400,
                           photo_height=300,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="tesy-invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# Результат после оплаты
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successfull_payment(message: types.Message):
    print("Success")
    payment_info = message.successful_payment.to_python()
    tranzaktion = ""
    for k, v in payment_info.items():
        if k == "telegram_payment_charge_id":
            tranzaktion = v
        print(f"{k} = {v}")
    print('\n')
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму <b>{message.successful_payment.total_amount // 100} "
                           f"{message.successful_payment.currency}</b> прошел успешно. "
                           f"Номер вашей транзакции {tranzaktion}. Приятного пользования!",
                           parse_mode="HTML",
                           reply_markup=kb_unreg
                           )

    # Изменение статуса
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    cursor.execute(f"""Update users set status = "paid", subscribe_start = "{date.today()}", 
                       subscribe_finish = "{next_month(date.today())}" 
                       where user_id = {message.from_user.id}""")
    conn.commit()
    cursor.close()


# Хендлер Возращения в меню
@dp.message_handler(Text(equals="В меню"))
async def menu_func(message: types.Message):
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM users WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if result[0] == "free":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню🦩",
                               parse_mode="HTML",
                               reply_markup=kb_free)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню🦩",
                               parse_mode="HTML",
                               reply_markup=kb_reg)


# Хендлер Предостережения
@dp.message_handler(Text(equals="❌Предостережения❌"))
async def predostr_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=PREDOSTR,
                           parse_mode="HTML")


# Хендлер Пользование ботом
@dp.message_handler(Text(equals="Как начать пользоваться ботом?"))
async def instruct_func(message: types.Message):
    await bot.send_video(chat_id=message.from_user.id,
                         video=open("imgs/CHANGE_TO_INSTRUCTION.mp4", "rb"),
                         caption="Подробная инструкция")


# !!!ПЛАТНЫЙ ФУНКЦИОНАЛ!!!
# Хендлер Авторизации
@dp.message_handler(Text(equals="Авторизация"))
async def auth_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите ваш <b>api_key</b>: ",
                           parse_mode="HTML")
    await Auth.api_key.set()


# Хендлер получения Api-key
@dp.message_handler(state=Auth.api_key)
async def set_api_key(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['api_key'] = message.text
        await Auth.api_secret.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите ваш <b>api_secret</b>: ",
                           parse_mode="HTML")


# Хендлер получения Api-secret
@dp.message_handler(state=Auth.api_secret)
async def set_api_secret(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['api_secret'] = message.text
        await state.finish()
    await bot.send_message(message.chat.id, 'Ваш профиль создан', reply_markup=kb_reg)

    # Запись Данных в бд
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    s = await state.get_data()
    cursor.execute(f"""UPDATE users SET api_secret = "{s.get("api_secret")}", api_key = "{s.get("api_key")}"
                           WHERE user_id = {message.from_user.id}""")
    conn.commit()
    cursor.close()


# Проверка на полную регистрацию
def api_stock(a):
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    return cursor.execute('SELECT api_secret FROM users WHERE user_id=?;', (a,)).fetchone()


# Хендлер Профиля
@dp.message_handler(Text(equals="Профиль"))
async def profile_func(message: types.Message):
    info = api_stock(message.from_user.id)
    if info is not None:
        await message.answer(text="Выберите действие", reply_markup=kb_profile)


# Хендлер Баланса
@dp.message_handler(Text(equals="Баланс"))
async def balance_func(message: types.Message):
    info = api_stock(message.from_user.id)
    if info is not None:
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        data = cursor.execute('SELECT api_secret, api_key FROM users WHERE user_id=?;', (message.from_user.id,)).fetchone()

        session = spot.HTTP(endpoint="https://api.bybit.com", api_key=data[1], api_secret=data[0])
        session1 = HTTP(endpoint="https://api.bybit.com", api_key=data[1], api_secret=data[0])
        balance = session1.get_wallet_balance()["result"]["USDT"]['available_balance']
        info = session.get_wallet_balance()["result"]["balances"]
        if len(info) != 0 and int(balance) != 0:
            coins_list = session.get_last_traded_price()["result"]["list"]
            total = 0
            text = ""
            for obj in info:
                for coin in coins_list:
                    if coin["symbol"] == f"{obj['coin']}USDT":
                        text += f"<b>{obj['coin']}</b>: {str(float(coin['price']) * float(obj['total']))} $\n"
                        total += float(coin["price"]) * float(obj["total"])
            total += balance
            text += f"<b>Стоимость всех активов</b>: {int(total * 100) / 100} $"
            await bot.send_message(chat_id=message.from_user.id,
                                   text=text,
                                   parse_mode="HTML")
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="На балансе нет средств")



# Хендлер хуйни
@dp.message_handler()
async def unknown_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Мы не предусмотрели данный запрос. Повторите попытку.")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
