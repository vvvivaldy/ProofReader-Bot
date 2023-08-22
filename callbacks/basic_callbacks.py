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

    label = f"Подписка на {callback.data}"
    if (PAYMENTS_TOKEN:=os.getenv('PAYMENTS_TOKEN')).split(":")[1] == "TEST":

        # Изменение цены при оплате по партнерке
        conn, cursor = db_connect()

        # Поиск приведенного пользователя человека (Если None - значит его никто не привел)
        partner = cursor.execute(f'SELECT id FROM ref_clients WHERE client_id = "{callback.from_user.id}"').fetchone()
        if partner != None:
            try:
                can_sale = cursor.execute(f'SELECT status, sale FROM referral WHERE id = "{partner[0]}"').fetchone()
                cursor.close()
                # Проверка партнера "на наличие в чс". Те,кто в чс или потеряли партнерку - со статусом block либо off
                if can_sale[0] == 'on':
                    PRICE = PRICE * (1 - can_sale[1]/100)
                    label = f"Подписка на {callback.data}. Скидка - {can_sale[1]}% от партнёра"
            except:
                pass
            
        #приведение цены в нужный вид
        PRICE = int(PRICE * 100)
        await bot.send_invoice(callback.from_user.id,
                           title="Подписка на ProofReader",
                           description=f"Активация подписки на {callback.data}",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://i.postimg.cc/zBynYjZq/photo-2023-06-18-16-59-44.jpg",
                           photo_height=200,
                           is_flexible=False,
                           prices=[types.LabeledPrice(label=label, amount=PRICE)],
                           start_parameter="ProofReader-subscription",
                           payload="tesy-invoice-payload")