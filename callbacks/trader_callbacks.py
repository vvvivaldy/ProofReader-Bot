from handlers.A_head_of_handlers import *

@dp.callback_query_handler(lambda c: c.data[0] == 'E')
async def trader_callbacks(callback: types.CallbackQuery):
    callback.data = callback.data[1:]
    match callback.data:
        case 'people':
            await callback.answer('Колво подписаных людей')

        case 'OpenOrders':
            await callback.answer('Открытые ордера')

        case 'HistoryOrders':
            await callback.answer('История ордеров')