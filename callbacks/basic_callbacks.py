from handlers.A_head_of_handlers import *


@dp.callback_query_handler(lambda c: c.data[0] == 'B')
async def pay(callback: types.CallbackQuery):
    callback.data = callback.data[1:]
    with open("db/prices.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter = ";")
        for row in file_reader:
            PRICES = [int(i) for i in row]
            print(PRICES)
            break
    if callback.data == '1 неделю':
        PRICE = PRICES[0]
    elif callback.data == '1 месяц':
        PRICE = PRICES[1]
    elif callback.data == '3 месяца':
        PRICE = PRICES[2]
    elif callback.data == '6 месяцев':
        PRICE = PRICES[3]
    elif callback.data == '1 год':
        PRICE = PRICES[4]
    if (PAYMENTS_TOKEN:=os.getenv('PAYMENTS_TOKEN')).split(":")[1] == "TEST":
        await bot.send_invoice(callback.from_user.id,
                           title="Подписка на ProofReader",
                           description=f"Активация подписки на {callback.data}",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://i.postimg.cc/zBynYjZq/photo-2023-06-18-16-59-44.jpg",
                           photo_height=200,
                           is_flexible=False,
                           prices=[types.LabeledPrice(label=f"Подписка на {callback.data}", amount=PRICE * 100)],
                           start_parameter="ProofReader-subscription",
                           payload="tesy-invoice-payload")