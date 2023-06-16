from data.imports import *

load_dotenv()

bot = Bot(os.getenv('TG_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


# Расшифровка
def decrypt_api(api):
    cipher = Fernet(bytes(os.getenv('CIPHER_KEY')+'=',encoding='utf-8'))
    return cipher.decrypt(api).decode('utf-8')


# Шифровка
def encrypt_api(api):
    cipher = Fernet(bytes(os.getenv('CIPHER_KEY')+'=',encoding='utf-8'))
    return cipher.encrypt(bytes(api,encoding='utf-8'))


# Дата конца подписки
def next_month(today):
    delta = timedelta(days=30)
    return today + delta