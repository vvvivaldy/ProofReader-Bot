from handlers.D_paid_function_handlers import *
from callbacks.trader_callbacks import *


class TempStream:
    def __init__(self, id, func):
        self.id = id
        self.func = func

    def create_order_in_object(self, ord, value, mode = False):
            conn, cursor = db_connect()
            text = ""
            if ord[0]["orderType"] == "Market":
                if len(ord) == 3:
                    tp = next((n for n in ord if n['stopOrderType'] == 'TakeProfit'), None)
                    sl = next((n for n in ord if n['stopOrderType'] == 'StopLoss'), None)

                    if ord[value]["takeProfit"] != "":
                        text = f"""РЫНОЧНАЯ ЗАЯВКА
                        
Монета: <b>{ord[value]["symbol"]}</b>
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
                        current_date = datetime.now().date()
                        current_date = current_date.strftime('%Y-%m-%d')
                        cursor.execute(f"INSERT INTO orders (order_id, tp_order_id, sl_order_id, trade_pair, take_profit, stop_loss, trader_id, user_id,"
                                    f" status, open_price, close_price, close_order_id, profit, qty, date_1) VALUES ('{ord[value]['orderId']}', "
                                    f"'{tp['orderId']}', '{sl['orderId']}' ,"
                                    f"'{ord[value]['symbol']}', '{ord[value]['takeProfit']}', '{ord[value]['stopLoss']}', "
                                    f"'{self.id}', '', 'open', '{ord[value]['cumExecValue']}', '', '', '', '{ord[value]['qty']}', '{current_date}');")
                        conn.commit()
                    else:
                        current_date = datetime.now().date()
                        cursor.execute(f"UPDATE orders SET take_profit = {ord[value]['takeProfit']}, stop_loss = {ord[value]['stopLoss']}, order_id = '{ord[value]['orderId']}', qty = qty + {ord[value]['qty']}, date_1 = '{current_date}' WHERE trader_id = {self.id} AND trade_pair = '{ord[value]['symbol']}' AND status = 'open'")
                        conn.commit()

                else:
                    requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                    f'/sendMessage?chat_id={self.id}&text=Вы не установили StopLoss или TakeProfit. Сделка не высветится у пользователей')
                    return

            elif ord[0]["orderType"] == "Limit":
                if ord[0]["takeProfit"] != "" and ord[0]["stopLoss"] != "":
                    text = f"""ЛИМИТНАЯ ЗАЯВКА
                    
Монета: <b>{ord[0]["symbol"]}</b>
Тип покупки: <b>{ord[0]["side"]}</b>
Количество: <b>{ord[0]["qty"]}</b>
Цена: <b>{ord[0]["price"]} $</b>
TakeProfit: <b>{ord[0]["takeProfit"]} $</b>
StopLoss: <b>{ord[0]["stopLoss"]} $</b>"""
                    if not mode:
                        current_date = datetime.now().date()
                        current_date = current_date.strftime('%Y-%m-%d')
                        cursor.execute(
                            f"INSERT INTO orders (order_id, tp_order_id, sl_order_id, trade_pair, take_profit, stop_loss, trader_id, user_id,"
                            f" status, open_price, close_price, close_order_id, profit, qty, date_1) VALUES ('{ord[0]['orderId']}', "
                            f"'', '' ,"
                            f"'{ord[0]['symbol']}', '{ord[0]['takeProfit']}', '{ord[0]['stopLoss']}', "
                            f"'{self.id}', '', 'open', '{ord[0]['price']}', '', '', '', '{ord[0]['qty']}', '{current_date}');")
                        conn.commit()
                        conn.close()
                    else:
                        current_date = datetime.now().date()
                        cursor.execute(
                            f"UPDATE orders SET take_profit = {ord[value]['takeProfit']}, stop_loss = {ord[value]['stopLoss']}, order_id = '{ord[value]['orderId']}', qty = qty + {ord[value]['qty']}, date_1 = '{current_date}' WHERE trader_id = {self.id} AND trade_pair = '{ord[value]['symbol']}' AND status = 'open'")
                        conn.commit()
                        conn.close()
                else:
                    requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                 f'/sendMessage?chat_id={self.id}&text=Вы не установили StopLoss или TakeProfit. Сделка не высветится у пользователей.')
                    return

            requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                         f'/sendMessage?chat_id={self.id}&text={text}&parse_mode=HTML')

    def handle_message(self, message):
        conn, cursor = db_connect()
        api_key, api_secret, webstream = cursor.execute(f'SELECT api_key,api_secret, webstream FROM traders WHERE trader_id = {self.id}').fetchall()[0]
        print(webstream)
        session = HTTP(
            testnet=False,
            api_key=decrypt_api(api_key),
            api_secret=decrypt_api(api_secret),
        )
        ord = message["data"]
        print(ord)
        # Индекс элемента списка, заполненного ордера
        value = next((ord.index(n) for n in ord if "orderStatus" in n and n["orderStatus"] == "Filled"), None)
        self.value = value
        self.ord = ord
        # Поиск открытых ордеров (сработанных)
        existence_validate_actual = bool(cursor.execute(f"SELECT count(*) FROM orders WHERE trader_id = '{self.id}' AND trade_pair = '{ord[0]['symbol']}' AND status = 'open' AND tp_order_id != '' AND sl_order_id != ''").fetchone()[0])
        existence_validate_limit = bool(cursor.execute(f"SELECT count(*) FROM orders WHERE trader_id = '{self.id}' AND trade_pair = '{ord[0]['symbol']}' AND status = 'open' AND tp_order_id == '' AND sl_order_id == ''").fetchone()[0])

        # Если есть открытый ордер, но отслеживание выключено
        if existence_validate_limit and webstream == 0:
            if ord[0]["orderType"] == "Limit" and ord[0]["orderStatus"] == "Cancelled":
                cursor.execute(f"DELETE FROM orders WHERE order_id = '{ord[0]['orderId']}'")
                conn.commit()
                conn.close()
                requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                             f'/sendMessage?chat_id={self.id}&text=Вы отменили ордер на покупку {ord[0]["symbol"]}.')
            return

        #Если есть открытый ордер этой монеты
        if existence_validate_actual:
            stop_orders = cursor.execute(f"SELECT tp_order_id, sl_order_id FROM orders WHERE trader_id = '{self.id}' AND trade_pair = '{ord[0]['symbol']}' AND status = 'open'").fetchone()
            tp_status = session.get_order_history(
                category="linear",
                orderId=stop_orders[0])['result']['list'][0]['orderStatus']
            sl_status = session.get_order_history(
                category="linear",
                orderId=stop_orders[1])['result']['list'][0]['orderStatus']
            
            if tp_status == 'Filled' or sl_status == 'Filled':
                so_status = 'Filled'
            elif tp_status == 'Deactivated' or sl_status == 'Deactivated':
                so_status = 'Deactivated'
            elif tp_status == 'Untriggered' or sl_status == 'Untriggered':
                so_status = 'Untriggered'

        # Если нет открытого ордера этой монеты
        if not existence_validate_actual and webstream == 1:
            self.create_order_in_object(ord, value)

        elif existence_validate_actual:
            if so_status == 'Deactivated':
                close_order = session.get_closed_pnl(
                    category="linear",
                    limit=1,
                )
                print(close_order)
                exit_price = close_order["result"]["list"][0]["avgExitPrice"]
                profit = str(round(float(close_order["result"]["list"][0]["closedPnl"]), 2))
                order_id = close_order["result"]["list"][0]["orderId"]
                cursor.execute(f'''UPDATE orders SET status = "closed",
                                profit = "{profit}", close_price = "{exit_price}", close_order_id = "{order_id}" WHERE trade_pair = "{ord[value]['symbol']}" AND 
                                trader_id = "{self.id}" AND status = "open"''')
                conn.commit()

                text = f"""Монета: <b>{ord[1]["symbol"]}</b>
Тип покупки: <b>{ord[value]["side"]}</b> 
Количество: <b>{ord[value]["qty"]}</b>
Цена: <b>{exit_price} $</b>
Профит: <b>{profit} $</b>"""
                
                requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                                    f'/sendMessage?chat_id={self.id}&text={text}&parse_mode=HTML')

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

        elif not existence_validate_actual and webstream == 0:
            requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                         f'/sendMessage?chat_id={self.id}&text=Ордер не был отправлен вашим подписчикам')


        cursor.close()
        self.func(self.id)
        requests.get(f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}' + \
                     f'/sendMessage?chat_id={self.id}&text=Отслеживание OFF❌&reply_markup={kb_trader}')
        

def tracking(id, conn, cursor, mode='off'):
    if mode == 'off':
        cursor.execute(f"UPDATE traders SET webstream = '0' WHERE trader_id = {id};")
    elif mode == 'on':
        cursor.execute(f"UPDATE traders SET webstream = '1' WHERE trader_id = {id};")
    conn.commit()
    cursor.close()


async def go_stream(id):
    conn, cursor = db_connect()
    api_key, api_secret = cursor.execute(f'SELECT api_key,api_secret FROM traders WHERE trader_id = {id}').fetchall()[0]
    ws = WebSocket(
    testnet=False,
    channel_type="private",
    api_key=decrypt_api(api_key),
    api_secret=decrypt_api(api_secret))

    tmp = TempStream(id, stop_stream)
    tracking(id, conn, cursor, 'off')
    global stream_websockets
    stream_websockets[f'stream_{id}'] = (ws, tmp)
    ws.order_stream(callback=tmp.handle_message)
    

def stop_stream(id):
    conn, cursor = db_connect()
    #FIXME ИЗМЕНИТЬ try except!!!
    try:
        cursor.execute(f"SELECT webstream FROM traders WHERE trader_id = '{id}'")
    except:
        return False
    tracking(id, conn, cursor)
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
        conn, cursor = db_connect()
        tracking(message.from_user.id, conn, cursor, mode="on")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отслеживание ON✅",
                               reply_markup=kb_trader2)
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
        
        