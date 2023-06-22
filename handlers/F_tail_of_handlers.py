from handlers.E_traders_panel_handlers import *



@dp.message_handler(Text(equals='Редактировать API'))
async def edit_api(message: types.Message):
    if paid_validate(message.from_user.id):
        pass
    elif trader_validate(message.from_user.id):
        pass
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Мы не предусмотрели данный запрос. Повторите попытку.')


# Хендлер хуйни
@dp.message_handler()
async def unknown_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Мы не предусмотрели данный запрос. Повторите попытку.")