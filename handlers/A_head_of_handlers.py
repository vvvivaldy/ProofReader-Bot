from data.imports import *

dotenv.load_dotenv(dotenv.find_dotenv())

bot = Bot(os.getenv('TG_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
admin_ids = (os.getenv('NIKITA_ID'), os.getenv('MISHA_ID'), os.getenv('ROMA_ID'))
stream_websockets = {}


# проверка на нужнуб клавиатуру трейдера
def true_kb(trader_id: int, mode = False) -> ReplyKeyboardMarkup:
    global stream_websockets
    if f'stream_{trader_id}' in stream_websockets and not mode:
        return kb_trader2
    return kb_trader


# проверка на трейдера
def trader_validate(user_id: int, mode=True) -> bool:
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    try:
        res = cursor.execute(f'SELECT status FROM traders WHERE trader_id={user_id};').fetchone()[0]
        if res == 'trader':
            return True
        elif res == 'block' and mode:
            requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}'
                         f'/sendMessage?chat_id={user_id}&text=Вы присутствуете в черном списке. Доступ '
                         f'запрещен.&reply_markup={ReplyKeyboardRemove()}')
        return False
    except Exception:
        return False


# Проверка на подписку
def paid_validate(user_id: int, mode=True) -> bool:
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    try:
        res = cursor.execute(f'SELECT status FROM users WHERE user_id={user_id};').fetchone()[0]
        if res == 'paid':
            return True
        elif res == 'block' and mode:
            requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}'
                         f'/sendMessage?chat_id={user_id}&text=Вы присутствуете в черном списке. Доступ '
                         f'запрещен. Обратитесь в тех. поддержку.&reply_markup={ReplyKeyboardRemove()}')
        return False
    except Exception:
        return False


# Подключение к бд
def db_connect():
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    return conn, cursor


# Расшифровка
def decrypt_api(api, key=None):
    if key is None:
        cipher = Fernet(bytes(os.getenv('CIPHER_KEY') + '=', encoding='utf-8'))
    else:
        cipher = Fernet(bytes(key + '=', encoding='utf-8'))
    if type(api) == bytes:
        return cipher.decrypt(api).decode('utf-8')
    return cipher.decrypt(bytes(api[2:-1], encoding='utf-8')).decode('utf-8')


# Шифровка
def encrypt_api(api):
    cipher = Fernet(bytes(os.getenv('CIPHER_KEY') + '=', encoding='utf-8'))
    return cipher.encrypt(bytes(api, encoding='utf-8'))


# Проверка на админа
async def admin_validate(message: types.Message):
    if str(message.from_user.id) in admin_ids:
        return True
    return False


# Дата конца подписки
def next_month(today):
    delta = timedelta(days=30)
    return today + delta


# Добавление нового пользователя в бд
async def db_validate(cursor, conn, message, info=None):
    if info is None:
        cursor.execute(
            f"""INSERT INTO users VALUES ('{message.from_user.id}', '0', '0', 'free', '', '', '', '', '', '1', 
            'false', '');""")
        cursor.execute("UPDATE counter SET count_users_all_time = count_users_all_time + 1")
        conn.commit()


def edit_status_ref(id, status, cursor):
        if bool(cursor.execute(f'SELECT 1 FROM ref_clients WHERE client_id = {id} LIMIT 1').fetchone()[0]):
            if status in ('paid','free'):
                cursor.execute(f'UPDATE ref_clients SET client_status = "{status}" WHERE client_id = {id}')
            elif status == 'trader':
                cursor.execute(f'DELETE FROM ref_clients WHERE client_id = {id}')

