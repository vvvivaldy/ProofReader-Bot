from handlers.B_basic_function_handlers import *

admin_ids = [os.getenv('NIKITA_ID'),os.getenv('MISHA_ID'),os.getenv('ROMA_ID')]


@dp.message_handler(commands=['ADMINPANEL'])
async def admin_validate(message: types.Message):
    if str(message.from_user.id) in admin_ids:
        print(f'Зашел админ {message.from_user.id}')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")