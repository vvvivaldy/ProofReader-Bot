from handlers.D_paid_function_handlers import *
from callbacks.trader_callbacks import *


class TempStream:
    def __init__(self, id, func):
        self.id = id
        self.func = func

    def create_order_in_object(self, ord, value, mode = False):
            conn, cursor = db_connect()
            if len(ord) == 3:
                tp = next((n for n in ord if n['stopOrderType'] == 'TakeProfit'), None)
                sl = next((n for n in ord if n['stopOrderType'] == 'StopLoss'), None)

                if ord[value]["takeProfit"] != "":
                    text = f"""Монета: <b>{ord[value]["symbol"]}</b>
Тип покупки: <b>{ord[value]["side"]}</b>
Количество: <b>{ord[value]["qty"]}</b>
Цена: <b>{ord[value]["cumExecValue"]} $</b>
TakeProfit: <b>{ord[value]["takeProfit"]} $</b>
StopLoss: <b>{ord[value]["stopLoss"]} $</b>"""
                else:
                    requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                f'/sendMessage?chat_id={self.id}&text=Напишите в тех поддержку об ошибке 908 и пришлите скриншот действий с ботом')
                    return
                if not mode:
                    cursor.execute(f"INSERT INTO orders (order_id, tp_order_id, sl_order_id, trade_pair, take_profit, stop_loss, trader_id, user_id,"
                                f" status, open_price, close_price, close_order_id, profit, qty) VALUES ('{ord[value]['orderId']}', "
                                f"'{tp['orderId']}', '{sl['orderId']}' ,"
                                f"'{ord[value]['symbol']}', '{ord[value]['takeProfit']}', '{ord[value]['stopLoss']}', "
                                f"'{self.id}', '', 'open', '{ord[value]['cumExecValue']}', '', '', '', '{ord[value]['qty']}');")
                    conn.commit()
                else:
                    cursor.execute(f"UPDATE orders SET take_profit = {ord[value]['takeProfit']}, stop_loss = {ord[value]['stopLoss']}, order_id = '{ord[value]['orderId']}', qty = qty + {ord[value]['qty']} WHERE trader_id = {self.id} AND trade_pair = '{ord[value]['symbol']}' AND status = 'open'")
                    conn.commit()

            else:
                requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                f'/sendMessage?chat_id={self.id}&text=Вы не установили StopLoss или TakeProfit. Сделка не высветится у пользователей')
                return
            requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                    f'/sendMessage?chat_id={self.id}&text={text}&parse_mode=HTML')

    def handle_message(self, message):
        ord = message["data"]
        value = next((ord.index(n) for n in ord if "orderStatus" in n and n["orderStatus"] == "Filled"), None)
        self.value = value
        self.ord = ord
        conn, cursor = db_connect()
        existence_validate = bool(cursor.execute(f"SELECT count(*) FROM orders WHERE trader_id = '{self.id}' AND trade_pair = '{ord[0]['symbol']}' AND status = 'open'").fetchone()[0])

        if existence_validate:
            stop_orders = cursor.execute(f"SELECT tp_order_id, sl_order_id FROM orders WHERE trader_id = '{self.id}' AND trade_pair = '{ord[0]['symbol']}' AND status = 'open'").fetchone()
            api_key, api_secret = cursor.execute(f'SELECT api_key,api_secret FROM traders WHERE trader_id = {self.id}').fetchall()[0]
            session = HTTP(
                testnet=False,
                api_key=decrypt_api(api_key),
                api_secret=decrypt_api(api_secret),
            )
            tp_status = session.get_order_history(
                category="linear",
                orderId = stop_orders[0])['result']['list'][0]['orderStatus']
            sl_status = session.get_order_history(
                category="linear",
                orderId = stop_orders[1])['result']['list'][0]['orderStatus']
            
            if tp_status == 'Filled' or sl_status == 'Filled':
                so_status = 'Filled'
            elif tp_status == 'Deactivated' or sl_status == 'Deactivated':
                so_status = 'Deactivated'
            elif tp_status == 'Untriggered' or sl_status == 'Untriggered':
                so_status = 'Untriggered'

            print(so_status)
                
        if not existence_validate:
            self.create_order_in_object(ord, value)
        else :
            if so_status == 'Deactivated':
                close_order = next((n for n in ord if "cumExecValue" in n and n["cumExecValue"] != "0"), None)
                price = close_order['cumExecValue']

                data = cursor.execute(f"SELECT qty, open_price FROM orders WHERE trade_pair = '{ord[value]['symbol']}' AND trader_id = '{self.id}' AND status = 'open'").fetchone()
                profit = round(float(price) * float(data[0]) - float(data[0]) * float(data[1]), 5)
                cursor.execute(f'''UPDATE orders SET status = "closed",
                                profit = "{profit}", close_price = "{price}", close_order_id = "{close_order['orderId']}" WHERE trade_pair = "{ord[value]['symbol']}" AND 
                                trader_id = "{self.id}" AND status = "open"''')
                conn.commit()

                text = f"""Монета: <b>{ord[1]["symbol"]}</b>
Тип покупки: <b>{ord[value]["side"]}</b> 
Количество: <b>{ord[value]["qty"]}</b>
Цена: <b>{price} $</b>
Профит: <b>{profit} $</b>"""
                
                requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                    f'/sendMessage?chat_id={self.id}&text={text}&parse_mode=HTML')

            #FIXME: добавить клавиатуру в два нижних элифа
            #FIXME: Поработать с антригер и тригер

            elif so_status == 'Untriggered':
                requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                f'/sendMessage?chat_id={self.id}&text=У ваших подписчиков в данный момент есть открытый вами ордер на данной валютной паре. Вероятно, Вы хотите докупить и/или изменить стоп-ордера. Вы хотите отправить им ТОЛЬКО ЧТО СОЗДАННЫЙ ВАМИ ордер, или не будете?&reply_markup={kb_order}')
                cursor.close()
                self.func(self.id)
                return

            elif so_status == 'Filled':
                print('Filled успешно сработало')
                if so_status == tp_status:
                    who = stop_orders[0]
                else:
                    who = stop_orders[1]
                close_order = next((n for n in ord if "cumExecValue" in n and n["cumExecValue"] != "0"), None)
                data = cursor.execute(f"SELECT qty, open_price FROM orders WHERE trade_pair = '{ord[value]['symbol']}' AND trader_id = '{self.id}' AND status = 'open'").fetchone()
                price = close_order['cumExecValue']
                profit = round(float(price) * float(data[0]) - float(data[0]) * float(data[1]), 5)
                cursor.execute(f'''UPDATE orders SET status = "closed",
                                profit = "{profit}", close_price = "{price}", close_order_id = "{who}" WHERE trade_pair = "{ord[value]['symbol']}" AND 
                                trader_id = "{self.id}" AND status = "open"''')

                conn.commit()
                self.create_order_in_object(ord, value)

        cursor.close()
        self.func(self.id)
        requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                            f'/sendMessage?chat_id={self.id}&text=Отслеживание OFF❌&reply_markup={kb_trader}')
        

def tracking(ws,tmpstream = None, mode = 'off'):
    if mode == 'off':
        ws.exit()
    elif mode == 'on' and isinstance(tmpstream, TempStream):
        ws.order_stream(callback=tmpstream.handle_message)
    else:
        raise Exception('Вы передали какую-то хуйню в функцию tracking')


async def go_stream(id):
    conn, cursor = db_connect()
    api_key, api_secret = cursor.execute(f'SELECT api_key,api_secret FROM traders WHERE trader_id = {id}').fetchall()[0]

    ws = WebSocket(
    testnet=False,
    channel_type="private",
    api_key=decrypt_api(api_key),
    api_secret=decrypt_api(api_secret))

    tmp = TempStream(id, stop_stream)
    tracking(ws, tmp, 'on')
    global stream_websockets
    stream_websockets[f'stream_{id}'] = (ws, tmp)

    await bot.send_message(chat_id=id,
                           text='Отслеживание ON✅',
                           reply_markup=kb_trader2)
    

def stop_stream(id):
    global stream_websockets
    try:
        ws = stream_websockets[f'stream_{id}'][0]
    except:
        return False
    tracking(ws)
    return True


@dp.message_handler(Text(equals='Ключи'))
async def keys(message: types.Message):
    if trader_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите действие",
                               reply_markup=kb_keys)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Вернуться'))
async def back(message: types.Message):
    if trader_validate(message.from_user.id):
        global stream_websockets
        if f'stream_{message.from_user.id}' in stream_websockets:
            await bot.send_message(chat_id=message.from_user.id,
                                text="Вы вернулись в меню",
                                reply_markup=kb_trader2)
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                text="Вы вернулись в меню",
                                reply_markup=kb_trader)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Создать ключ'))
async def new_key(message: types.Message):
    if trader_validate(message.from_user.id):
        letters = string.ascii_lowercase
        key = ''.join(random.choice(letters) for i in range(8))

        with open('cache/keys.txt', 'w') as file:
            file.write(key)

        conn, cursor = db_connect()
        cursor.execute(f"INSERT INTO trader_keys (trader_id, key) VALUES ('{message.from_user.id}', '{key}');")
        conn.commit()
        cursor.close()

        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите количество активаций.",
                               reply_markup=ikb_quantity)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Удалить ключ'))
async def del_key(message: types.Message):
    if trader_validate(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите ключ, который необходимо удалить")
        await Key_Delete.key.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Вывод всех ключей'))
async def view_keys(message: types.Message):
    if trader_validate(message.from_user.id):
        conn, cursor = db_connect()
        text = "🗝 <b>КЛЮЧ</b> | <em>ДАТА</em> | <u>КОЛ-ВО АКТИВАЦИЙ</u> \n\n"
        data = cursor.execute(
            f"SELECT key, duration, quantity, quantity_tek FROM trader_keys WHERE trader_id = {message.from_user.id}").fetchall()
        for obj in data:
            text += f"<b>{data.index(obj) + 1}. {obj[0]}</b> | <em>{obj[1]}</em> | <u>{obj[3]}/{obj[2]}</u>\n"
        await bot.send_message(chat_id=message.from_user.id,
                               text=text,
                               parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Статистика Профиля'))
async def prof_stat(message: types.Message):
    if trader_validate(message.from_user.id):
        await bot.send_video(chat_id=message.from_user.id,
                             video='https://c.mql5.com/1/78/open-uri20150119-12-2b4861__1.gif',
                             caption='Статистика Профиля',
                             reply_markup=ikb_trader_stat)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Помощь'))
async def trader_help(message: types.Message):
    if trader_validate(message.from_user.id):
        kb_trader = true_kb(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text=TRADER_HELP,
                               parse_mode='html',
                               reply_markup=kb_trader)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Вкл отслеживание'))
async def trader_on(message: types.Message):
    if trader_validate(message.from_user.id):
        await go_stream(message.from_user.id)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")


@dp.message_handler(Text(equals='Выкл отслеживание'))
async def trader_off(message: types.Message):
    if trader_validate(message.from_user.id):
        if stop_stream(message.from_user.id):
            await bot.send_message(chat_id=message.from_user.id,
                           text='Отслеживание OFF❌',
                           reply_markup=kb_trader)
        else:
            await bot.send_message(chat_id=message.from_user.id,
                           text='Отслеживание и так выключено',
                           reply_markup=kb_trader)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Мы не предусмотрели данный запрос. Повторите попытку.")
        
        