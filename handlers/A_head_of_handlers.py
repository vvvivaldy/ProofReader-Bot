from data.imports import *

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

bot = Bot(os.getenv('TG_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
admin_ids = [os.getenv('NIKITA_ID'),os.getenv('MISHA_ID'),os.getenv('ROMA_ID')]

# Расшифровка
def decrypt_api(api, key=None):
    if key == None:
        cipher = Fernet(bytes(os.getenv('CIPHER_KEY')+'=',encoding='utf-8'))
    else:
        cipher = Fernet(bytes(key+'=',encoding='utf-8'))
    if type(api) == bytes:
        return cipher.decrypt(api).decode('utf-8')
    return cipher.decrypt(bytes(api[2:-1],encoding='utf-8')).decode('utf-8')


# Шифровка
def encrypt_api(api):
    cipher = Fernet(bytes(os.getenv('CIPHER_KEY')+'=',encoding='utf-8'))
    return cipher.encrypt(bytes(api,encoding='utf-8'))


# Проверка на админа
async def admin_validate(message: types.Message):
    if str(message.from_user.id) in admin_ids: return True
    return False


# Дата конца подписки
def next_month(today):
    delta = timedelta(days=30)
    return today + delta


# Проверка профиля а БД
async def db_validate(cursor, conn, message, info=None):
    # Если нет в бд
    if info is None:
        cursor.execute(f"""INSERT INTO users VALUES ('{message.from_user.id}', '0', '0', 'free', '', '', '');""")
        cursor.execute("UPDATE counter SET count_users_all_time = count_users_all_time + 1")
        conn.commit()
    # Если есть в бд
    else:
        cursor.execute("SELECT status, api_key FROM users WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        # Если статус бесплатный
        if result[0] == "free":
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Мы нашли вашу учетную запись в базе данных.",
                                   reply_markup=kb_free)
        # Если статус платный
        elif result[0] == "paid":
            if result[1] == "":
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Мы нашли вашу учетную запись в базе данных.",
                                       reply_markup=kb_unreg)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Мы нашли вашу учетную запись в базе данных.",
                                       reply_markup=kb_reg)