from handlers.A_head_of_handlers import *

@dp.callback_query_handler(lambda c: c.data[0] == 'C')
async def admin_callbacks(callback: types.CallbackQuery):
    callback.data = callback.data[1:]
    match callback.data:
        case 'uat':
            await callback.answer(text='хуяк,ты нажал на вывод статистики обо всех')

        case 'new':
            await callback.answer(text='еблысь,ты нажал на вывод статистики о новых перцах')

        case 'trans':
            await callback.answer(text='пиздяк, файл о всех покупах подписок и регистрации трейдеров')

        case 'edit':
            await callback.message.answer(text=
                                             'Следующим сообщением введите через ПРОБЕЛ цены для\n'
                                             '1 недели\n'
                                             '1 месяца\n'
                                             '3 месяцев\n'
                                             '6 месяцев\n'
                                             '1 года')
        case 'return':
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Вернулись назад',
                               reply_markup=kb_admin)
            await callback.message.delete()