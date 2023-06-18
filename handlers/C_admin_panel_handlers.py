from handlers.B_basic_function_handlers import *
from callbacks.admin_callbacks import *

admin_ids = [os.getenv('NIKITA_ID'),os.getenv('MISHA_ID'),os.getenv('ROMA_ID')]

async def admin_validate(message: types.Message):
    if str(message.from_user.id) in admin_ids: return True
    return False

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



@dp.message_handler(Text(equals='Цены'))
async def _(message: types.Message):
    pass


@dp.message_handler(Text(equals='Черный список'))
async def _(message: types.Message):
    pass


@dp.message_handler(Text(equals='Вывод данных о клиенте'))
async def _(message: types.Message):
    pass


@dp.message_handler(Text(equals='Выдать статус'))
async def _(message: types.Message):
    pass


@dp.message_handler(Text(equals='Перешифровка'))
async def _(message: types.Message):
    pass