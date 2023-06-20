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
        
@dp.message_handler(Text(equals='Статистика'))
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


@dp.message_handler(Text(equals='Вывод данных о клиенте'))
async def _(message: types.Message):
    pass


@dp.message_handler(Text(equals='Выдать статус'))
async def _(message: types.Message):
    pass


@dp.message_handler(Text(equals='Перешифровка'))
async def re_encrypt_api(message: types.Message):
    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    data = cur.execute('SELECT user_id, api_key, api_secret FROM users WHERE api_key != "";').fetchall()
    if len(data) > 0:
        try:
            tmp_key = os.getenv('CIPHER_KEY')
            decrypt_api(data[0][1],tmp_key)
        except InvalidToken:
            await bot.send_message(chat_id=message.from_user.id,
                                text=f'Произошла ошибка InvalidToken (какие-то api расшифровываются по старому ключу)')
            return
        dotenv.set_key(dotenv_file,'CIPHER_KEY',str(Fernet.generate_key())[2:-2],encoding='utf-8')
        for user in data:
            cur.execute(f'''UPDATE users SET api_key = "{encrypt_api(decrypt_api(user[1],tmp_key))}",
                                            api_secret = "{encrypt_api(decrypt_api(user[2],tmp_key))}" 
                                            WHERE user_id = {user[0]}''')
            conn.commit()

        await bot.send_message(chat_id=message.from_user.id,
                                text='Все api перекодированы')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                         text='База данных пуста')


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