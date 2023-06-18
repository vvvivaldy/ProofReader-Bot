from handlers.A_head_of_handlers import *

@dp.callback_query_handler()
async def admin_callbacks(callback: types.CallbackQuery):
    if callback.data == 'uat':
        await callback.answer(text='хуяк,ты нажал на вывод статистики обо всех')
    elif callback.data == 'new':
        await callback.answer(text='еблысь,ты нажал на вывод статистики о новых перцах')
    elif callback.data == 'trans':
        await callback.answer(text='пиздяк, файл о всех покупах подписок и регистрации трейдеров')
