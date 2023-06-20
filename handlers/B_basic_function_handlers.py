from handlers.A_head_of_handlers import *
from callbacks.basic_callbacks import *

# Хендлер старта
@dp.message_handler(commands=["start"])
async def start_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Приветствуем, {message.from_user.username}! В нашем боте вы сможете использовать те же ордера, что и профессиональные трейдеры на Bybit!. "
                                f"Подробнее ты можешь узнать нажав  "
                                f"на кнопку \"Описание\"",
                           reply_markup=kb_free)
    # Подключение к бд
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    info = cursor.execute('SELECT * FROM users WHERE user_id=?;', (message.from_user.id, )).fetchone()
    await db_validate(cursor, conn, message, info)
    await message.delete()



# Хендлер Описания
@dp.message_handler(Text(equals="Описание"))
async def descr_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=DESCR, parse_mode="HTML")



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
    if os.getenv('PAYMENTS_TOKEN').split(":")[1] == "TEST":
        await bot.send_photo(message.chat.id,
                             photo='https://i.postimg.cc/zBynYjZq/photo-2023-06-18-16-59-44.jpg',
                             caption="Тестовый платеж",
                             reply_markup=paykb)
    

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)



# Результат после оплаты
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successfull_payment(message: types.Message):
    print("Success")
    payment_info = message.successful_payment.to_python()
    tranzaktion = ""
    # Цены
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
    # Изменение статуса и количества подписанных
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    date_start = date.today()
    current_time = datetime.now().time()
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return date(year, month, day)
    if message.successful_payment.total_amount // 100 == 1490:
        date1 = "week"
        date_fininsh = date_start + timedelta(days=7)
    elif message.successful_payment.total_amount // 100 == 4490:
        date1 = "month"
        days = calendar.monthrange(date_start.year, date_start.month)[1]
        date_fininsh = date_start + timedelta(days=days)
    elif message.successful_payment.total_amount // 100 == 9990:
        date1 = "3_month"
        date_fininsh = add_months(date_start, 3)
    elif message.successful_payment.total_amount // 100 == 14990:
        date1 = "6_month"
        date_fininsh = add_months(date_start, 6)
    elif message.successful_payment.total_amount // 100 == 24990:
        date1 = "year"
        date_fininsh = str(add_months(date_start, 12))
    cursor.execute(f"""UPDATE users SET subscriptions = "{date1}" WHERE user_id = {message.from_user.id}""")
    cursor.execute(f"""INSERT or REPLACE into purchase_history VALUES ('{date_start}', '{current_time}', '{message.from_user.id}', '{date1}', '{message.successful_payment.total_amount // 100}', '{tranzaktion}')""")
    cursor.execute(f"""Update users set status = "paid", subscribe_start = "{date_start}", 
                       subscribe_finish = "{date_fininsh}" 
                       where user_id = {message.from_user.id}""")
    
    
    
    '''if message.successful_payment.total_amount // 100 == 1490:
        cursor.execute("UPDATE counter SET count_subs_week = count_subs_week + 1")
        week = "week"
        cursor.execute(f"""UPDATE users SET subscriptions = "{week}" WHERE user_id = {message.from_user.id}""")
        cursor.execute(f"""Update users set status = "paid", subscribe_start = "{date.today()}", 
                       subscribe_finish = "{date.today() + timedelta(days=7)}" 
                       where user_id = {message.from_user.id}""")
    elif message.successful_payment.total_amount // 100 == 4490:
        cursor.execute("UPDATE counter SET count_subs_month = count_subs_month + 1")
        month = "month"
        cursor.execute(f"""UPDATE users SET subscriptions = "{month}" WHERE user_id = {message.from_user.id}""")
        cursor.execute(f"""Update users set status = "paid", subscribe_start = "{date.today()}", 
                       subscribe_finish = "{next_month(date.today())}" 
                       where user_id = {message.from_user.id}""")
    elif message.successful_payment.total_amount // 100 == 9990:
        cursor.execute("UPDATE counter SET count_subs_3_month = count_subs_3_month + 1")
        month_3 = "3_month"
        cursor.execute(f"""UPDATE users SET subscriptions = "{month_3}" WHERE user_id = {message.from_user.id}""")
    elif message.successful_payment.total_amount // 100 == 14990:
        cursor.execute("UPDATE counter SET count_subs_6_month = count_subs_6_month + 1")
        month_6 = "6_month"
        cursor.execute(f"""UPDATE users SET subscriptions = "{month_6}" WHERE user_id = {message.from_user.id}""")
    elif message.successful_payment.total_amount // 100 == 24990:
        cursor.execute("UPDATE counter SET count_subs_1_year = count_subs_1_year + 1")
        year = "year"
        cursor.execute(f"""UPDATE users SET subscriptions = "{year}" WHERE user_id = {message.from_user.id}""")'''
    conn.commit()
    cursor.close()



# Хендлер Возращения в меню
@dp.message_handler(Text(equals="В меню"))
async def menu_func(message: types.Message):
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status, api_key FROM users WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if result[0] == "free":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню",
                               parse_mode="HTML",
                               reply_markup=kb_free)
    elif result[0] == "paid" and result[1] != "":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню",
                               parse_mode="HTML",
                               reply_markup=kb_reg)
    elif result[0] == "paid" and result[1] == "":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вернулись в меню",
                               parse_mode="HTML",
                               reply_markup=kb_unreg)



# Хендлер Предостережения
@dp.message_handler(Text(equals="❌Предостережения❌"))
async def predostr_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=PREDOSTR,
                           parse_mode="HTML")



# Хендлер Пользование ботом
@dp.message_handler(Text(equals="Как создать API ключ?"))
async def instruct_func(message: types.Message):
    await bot.send_video(chat_id=message.from_user.id,
                         video=open("imgs/instruct.mp4", "rb"),
                         caption="Подробная инструкция")