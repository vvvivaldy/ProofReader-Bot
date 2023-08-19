from handlers.B_basic_function_handlers import *
from callbacks.admin_callbacks import *



@dp.message_handler(commands=['ADMINPANEL'])
async def admin_check(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет, Хозяин...',
                               reply_markup=kb_admin)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        

@dp.message_handler(Text(equals='Статистика бота'))
async def statistics_for_admin(message: types.Message):
    if await admin_validate(message):
        await bot.send_photo(chat_id=message.from_user.id,
                             photo='https://avatars.mds.yandex.net/i?id=a3fee7ff2c0b3d36240e784b54605fa23e815401-9284609-images-thumbs&n=13',
                             reply_markup=ikas)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Цены'))
async def set_price(message: types.Message):
    if await admin_validate(message):
        await message.delete()
        with open("db/prices.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter = ";")
            for row in file_reader:
                PRICES = [i for i in row]
                PRICES = f'''1 неделя: {PRICES[0]}
1 месяц: {PRICES[1]}
3 месяца: {PRICES[2]}
6 месяцев: {PRICES[3]}
1 год: {PRICES[4]}'''
                break
        
        await bot.send_message(chat_id=message.from_user.id,
                               text=str(PRICES),
                               reply_markup=inl_kb_pr)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.") 


# Черный список
@dp.message_handler(Text(equals='Черный список'))
async def black_list(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите действие",
                               reply_markup=kb_black_list)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Посмотреть заблокированных'))
async def check_bl(message: types.Message):
    if await admin_validate(message):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        users = cursor.execute('SELECT * FROM black_list').fetchall()
        text = """"""
        for obj in users:
            text += f"{users.index(obj) + 1}. <b>{obj[0]}</b>, <b>{obj[1]}</b>\n"
        if text != "":
            await bot.send_message(chat_id=message.from_user.id,
                                   text=text,
                                   parse_mode="HTML",
                                   reply_markup=kb_black_list)
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Черный список пуст.",
                                   reply_markup=kb_black_list)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Добавить в чс'))
async def check_bl(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберете статус пользователя.",
                               reply_markup=inl_kb_status)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Удалить из чс'))
async def check_bl(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите id пользователя")
        await UserDel.id.set()

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Назад в админку'))
async def check_bl(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы в главном меню админки",
                               reply_markup=kb_admin)

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Вывод данных о клиенте'))
async def client_status(message: types.Message):
    await message.answer(text='Кого выбираем?',
                         reply_markup=ikk)


@dp.message_handler(Text(equals='Выдать статус'))
async def set_status(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Введите user_id которому надо выдать статус: ')
        await SetUserSubscriptionStatus.sub_status.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Перешифровка'))
async def re_encrypt_api(message: types.Message):
    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    data_user = cur.execute('SELECT user_id, api_key, api_secret FROM users WHERE api_key != "";').fetchall()
    data_trader = cur.execute('SELECT trader_id, api_key, api_secret FROM traders WHERE api_key != "";').fetchall()
    tmp_key = os.getenv('CIPHER_KEY')
    if len(data_user) > 0:
        try:
            decrypt_api(data_user[0][1],tmp_key)
        except InvalidToken:
            await bot.send_message(chat_id=message.from_user.id,
                                text=f'Произошла ошибка InvalidToken (какие-то api расшифровываются по старому ключу) в базе юзеров')
            return
        tmp = os.environ['CIPHER_KEY'] = str(Fernet.generate_key())[2:-2]
        dotenv.set_key('.env','CIPHER_KEY',tmp,encoding='utf-8')
        tmp = None
        for user in data_user:
            cur.execute(f'''UPDATE users SET api_key = "{encrypt_api(decrypt_api(user[1],tmp_key))}",
                                            api_secret = "{encrypt_api(decrypt_api(user[2],tmp_key))}" 
                                            WHERE user_id = {user[0]}''')
            conn.commit()

        await bot.send_message(chat_id=message.from_user.id,
                                text='Все api юзеров перекодированы')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                         text='База данных клиентов пуста')
    
    if len(data_trader) > 0:
        try:
            decrypt_api(data_trader[0][1],tmp_key)
        except InvalidToken:
            await bot.send_message(chat_id=message.from_user.id,
                                text=f'Произошла ошибка InvalidToken (какие-то api расшифровываются по старому ключу) в базе трейдеров')
            return
        
        if len(data_user) == 0:
            tmp = os.environ['CIPHER_KEY'] = str(Fernet.generate_key())[2:-2]
            dotenv.set_key('.env','CIPHER_KEY',tmp,encoding='utf-8')
            tmp = None

        for trader in data_trader:
            cur.execute(f'''UPDATE traders SET api_key = "{encrypt_api(decrypt_api(trader[1],tmp_key))}",
                                            api_secret = "{encrypt_api(decrypt_api(trader[2],tmp_key))}" 
                                            WHERE trader_id = {trader[0]}''')
            conn.commit()

        await bot.send_message(chat_id=message.from_user.id,
                                text='Все api трейдеров перекодированы')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                         text='База данных трейдеров пуста')


@dp.message_handler(lambda m: all([i.isdigit() for i in m.text[1:].split()]) and m.text[0] == '!')
async def edit_price(message: types.Message):
    if await admin_validate(message):
        message.text = message.text[1:]
        if all([i.isdigit for i in message.text.split()]) and len(list(message.text.split())) == 5 and all([int(i)>9 for i in message.text.split()]):
            new_prices = list(message.text.split())
            with open('db/prices.csv',mode = 'w', encoding='utf-8') as data:
                file_writer = csv.writer(data, delimiter=';',lineterminator='\r')
                file_writer.writerow(new_prices)
            await message.answer(text='Цены успешно изменены',
                                reply_markup=kb_admin)
        else:
            await message.answer(text='Введены неверные значения',
                                                reply_markup=inl_kb_pr)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.") 
        

@dp.message_handler(state=SetUserSubscriptionStatus.sub_status)
async def SetUserSubStatus(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['sub_status'] = message.text
    s = await state.get_data()
    try:
        user = s['sub_status']
    except:
        await bot.send_message(chat_id=message.from_user.id,
                text='Вы только что вводили этого пользователя. Повторите если вы не ошиблись',
                reply_markup=kb_admin)
        await state.reset_state()
        await state.finish()
        return
    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    try:
        user_db = cur.execute(f'SELECT user_id, status FROM users WHERE user_id = {user}').fetchall()
        if len(user_db) == 0:
            user_db = cur.execute(f'SELECT trader_id, status FROM traders WHERE trader_id = {user}').fetchall()
    except:
        await bot.send_message(chat_id=message.from_user.id,
                        text='Неккоректные данные в введенном id',
                        reply_markup=kb_admin)
        await state.reset_state()
        await state.finish()
        return
    cur.close()
    if user.isdigit() and len(user_db)>0:
        with open('cache/cache.txt','w',encoding='utf-8') as data:
            data.writelines([user])
        await bot.send_message(chat_id=message.from_user.id,
                                text=f'Статус юзера {user}: {user_db[0][1]}',
                                reply_markup=ikst)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                                text='Введены неккоректные данные или такого юзера не существует в бд',
                                reply_markup=kb_admin)
    await state.reset_state()
    await state.finish()


@dp.message_handler(Text(equals='Изменить % (ref)'))
async def pr_ref(message: types.Message):
    if await admin_validate(message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите число-процент скидки юзеров с партнерки (последний символ - %)",
                               reply_markup=kb_admin) 
        await Set_Procent.pr.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.") 
        

@dp.message_handler(state=Set_Procent.pr)
async def SetUserSubStatus(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['pr'] = message.text
    s = await state.get_data()
    s = s['pr']
    if s[-1]=='%' and s[:-1].isdigit() and 1<=float(s[:-1])<=99:
        dotenv.set_key('.env','PROCENT',s[:-1])
        os.environ['Procent'] = s[:-1]
        print(os.environ["Procent"])
        await bot.send_message(chat_id=message.from_user.id,
                               text="Успешно изменен процент",
                               reply_markup=kb_admin) 
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Неверное значение",
                               reply_markup=kb_admin) 
    await state.reset_state()
    await state.finish()