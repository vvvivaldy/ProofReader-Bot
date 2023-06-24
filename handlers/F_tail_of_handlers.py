from handlers.E_traders_panel_handlers import *



@dp.message_handler(Text(equals='Редактировать API'))
async def edit_api(message: types.Message):
    if paid_validate(message.from_user.id):
        conn , cursor = db_connect()
        res = cursor.execute(f'SELECT api_key,api_secret FROM users WHERE user_id = {message.from_user.id}').fetchone()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваш текущие \napi key: {decrypt_api(res[0])}\n\napi secret: {decrypt_api(res[1])}',
                               reply_markup=ik_edit_api)
    elif trader_validate(message.from_user.id):
        conn , cursor = db_connect()
        res = cursor.execute(f'SELECT api_key,api_secret FROM traders WHERE trader_id = {message.from_user.id}').fetchone()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваш текущие \napi key: {decrypt_api(res[0])}\n\napi secret: {decrypt_api(res[1])}',
                               reply_markup=ik_edit_api)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Мы не предусмотрели данный запрос. Повторите попытку.')


# Хендлер хуйни
@dp.message_handler()
async def unknown_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Мы не предусмотрели данный запрос. Повторите попытку.")