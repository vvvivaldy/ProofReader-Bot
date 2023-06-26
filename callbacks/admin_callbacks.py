import sqlite3

from handlers.A_head_of_handlers import *


def help_func(tek_date, total_dates_list, previous):
    tek_date = t.strptime(str(tek_date.date()), "%Y-%m-%d")
    total_list = [obj for obj in total_dates_list if (obj >= previous) and obj <= tek_date]
    return len(total_list)


def date_func(gap):
    tek_date = datetime.now()
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    dates_list = cursor.execute("SELECT subscribe_start FROM users WHERE subscribe_start IS NOT NULL OR "
                                "subscribe_start != '';").fetchall()
    total_dates_list = [t.strptime(i[0], "%Y-%m-%d") for i in dates_list]
    match gap:
        case "day":
            previous = t.strptime(str((tek_date - timedelta(days=1)).date()), "%Y-%m-%d")
            return help_func(tek_date, total_dates_list, previous)
        case "week":
            previous = t.strptime(str((tek_date - timedelta(days=7)).date()), "%Y-%m-%d")
            return help_func(tek_date, total_dates_list, previous)
        case "month":
            previous = t.strptime(str((tek_date - timedelta(days=30)).date()), "%Y-%m-%d")
            return help_func(tek_date, total_dates_list, previous)
        case "year":
            previous = t.strptime(str((tek_date - timedelta(days=365)).date()), "%Y-%m-%d")
            return help_func(tek_date, total_dates_list, previous)


@dp.callback_query_handler(lambda c: c.data[0] == 'C')
async def admin_callbacks(callback: types.CallbackQuery,):
    callback.data = callback.data[1:]
    match callback.data:
        case 'uat':
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT count_users_all_time, count_traders_all_time, count_subs_month, count_subs_3_month, count_subs_6_month, count_subs_1_year, count_subs_week FROM counter")
            result = cursor.fetchall()
            users = result[0][0]
            traders = result[0][1]
            users_month = result[0][2]
            users_3_month = result[0][3]
            users_6_month = result[0][4]
            users_1_year = result[0][5]
            users_week = result[0][6]
            text1 = f'Всего пользователей: <b>{users}</b>\nВсего трейдеров: <b>{traders}</b>\nПодписок на неделю: <b>{users_week}</b>\nПодписок на месяц: <b>{users_month}</b>\nПодписок на 3 месяца: {users_3_month}\nПодписок на 6 месяцев: <b>{users_6_month}</b>\nПодписок на год: <b>{users_1_year}</b>'
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=text1, parse_mode="HTML")
            conn.commit()
            cursor.close()
        case 'new':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Выберите период.", parse_mode="HTML",
                                   reply_markup=ikb_period)
        case 'day':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f"Новых пользователей за день: <b>{date_func('day')}</b>", parse_mode="HTML")

        case 'week':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f"Новых пользователей за неделю: <b>{date_func('week')}</b>", parse_mode="HTML")
        case 'month':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f"Новых пользователей за месяц: <b>{date_func('month')}</b>", parse_mode="HTML")
        case 'year':
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f"Новых пользователей за год: <b>{date_func('year')}</b>", parse_mode="HTML")

        case 'trans':
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT date, user_id, amount, [transaction] FROM purchase_history")
            result = cursor.fetchall()
            text2 = ''
            for i in range(len(result)):
                date2 = result[i][0]
                user_id2 = result[i][1]
                amount2 = result[i][2]
                tranzaktion = result[i][3]
                text2 += f'<b>Дата:</b> {date2}\n<b>Айди:</b> {user_id2}\n<b>Количество:</b> {amount2}\n<b>Номер транзакции:</b> {tranzaktion}\n\n\n'
            await bot.send_message(chat_id=callback.from_user.id, text=text2, parse_mode="HTML")
            cursor.close()

        case 'edit':
            await callback.message.answer(text=
                                             'Следующим сообщением введите первый символ "!" и через ПРОБЕЛ цены для\n'
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

        case 'Trader':
            await callback.message.answer(text="Введите id трейдера")
            await Bl_Id_Trader.id.set()

        case 'User':
            await callback.message.answer(text="Введите id юзера")
            await Bl_Id_User.id.set()

        case 'trader_status':
            await callback.message.answer('Введите id трейдера: ')
            await TraderStatus.status.set()

        case 'user_status':
            await callback.message.answer('Введите id пользователя: ')
            await UserStatus.status.set()

        case 'set_free':
            with open('cache/cache.txt','r',encoding='utf-8')as data:
                try:
                    data = data.readlines()[0]
                    conn = sqlite3.connect('db/database.db')
                    res = await set_user_status(conn,data,'free')
                    if res:
                        await callback.message.edit_text(text=f'Статус юзера {data}: free',
                                                        reply_markup=ikst)
                        cursor = conn.cursor()
                        cursor.execute(f'UPDATE users SET api_key = "", api_secret = "" WHERE user_id = "{data}"')
                        conn.commit()
                        cursor.close()
                    else:
                        await callback.message.edit_text(text=f'Не удалось обновить статус юзера {data}',
                                                        reply_markup=ikst)
                except:
                    print('Что-то с кэшом')
        
        case 'set_paid':
            with open('cache/cache.txt','r',encoding='utf-8')as data:
                try:
                    data = data.readlines()[0]
                    conn = sqlite3.connect('db/database.db')
                    res = await set_user_status(conn,data,'paid')
                    if res:
                        await callback.message.edit_text(text=f'Статус юзера {data}: paid',
                                                        reply_markup=ikst)
                    else:
                        await callback.message.edit_text(text=f'Не удалось обновить статус юзера {data}',
                                                        reply_markup=ikst)
                except:
                    print('Что-то с кэшом')

        case 'set_trader':
            with open('cache/cache.txt', 'r', encoding='utf-8') as data:
                try:
                    data = data.readlines()[0]
                    conn = sqlite3.connect('db/database.db')
                    res = await set_trader_status(conn, data, 'trader')
                    if res:
                        await callback.message.edit_text(text=f'Статус юзера {data}: trader',
                                                         reply_markup=ikst)
                    else:
                        await callback.message.edit_text(text=f'Не удалось обновить статус юзера {data}',
                                                         reply_markup=ikst)
                except:
                    print('Что-то с кэшом')


@dp.message_handler(state=UserStatus.status)
async def check_trader_status(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['status'] = message.text
    s = await state.get_data()
    user_id = s['status']
    if not all([i.isdigit() for i in user_id]):
        await bot.send_message(chat_id=message.from_user.id, text='Некорректные данные')
        await state.reset_state()
        return
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    result = cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id};').fetchall()
    if len(result) == 0:
        await bot.send_message(chat_id=message.from_user.id,
                         text='Такого пользователя нет')
        await state.reset_state()
        await state.finish()
        return 
    elif result[0][1] != None:
        api=(result[0][4][-5:],result[0][5][-5:])
    else:
        api=(None,None)
    await bot.send_message(chat_id=message.from_user.id,
                            text=f'''id: {result[0][0]}\r\n
sub_start: {result[0][1]}\r\n
sub_end: {result[0][2]}\r\n
status: {result[0][3]}\r\n
api_key: {api[0]}\r\n
api_secret: {api[1]}\r\n
subsribsions: {result[0][6]}\r\n
transaction: {result[0][7]}''')

    cursor.close()
    await state.reset_state()
    await state.finish()


@dp.message_handler(state=TraderStatus.status)
async def check_trader_status(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['status'] = message.text
    s = await state.get_data()
    trader_id = s['status']
    if not all([i.isdigit() for i in trader_id]):
        await bot.send_message(chat_id=message.from_user.id, text='Некорректные данные')
        await state.reset_state()
        await state.finish()
        return
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    result = cursor.execute(f'SELECT * FROM traders WHERE trader_id = {trader_id};').fetchall()
    if len(result) == 0:
        await bot.send_message(chat_id=message.from_user.id,
                         text='Такого трейдера нет')
        await state.reset_state()
        await state.finish()
        return 
    elif result[0][1] != None:
        api=(result[0][1][-5:],result[0][2][-5:])
    else:
        api=(None,None)

    await bot.send_message(chat_id=message.from_user.id,
                            text=f'''id: {result[0][0]}\r\n
api_key: {api[0]}\r\n
api_secret: {api[1]}\r\n
subscribers: {result[0][3]}\r\n
history: {result[0][4]}\r\n
trader_keys: {result[0][5]}''')
    cursor.close()
    await state.reset_state()
    await state.finish()


@dp.message_handler(state=Bl_Id_Trader.id)
async def add_trader(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['id'] = message.text
    s = await state.get_data()
    try:
        trader_id = s['id']
        try:
            trader_id = int(trader_id)
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute(f"""INSERT INTO black_list VALUES ('{trader_id}', 'trader');""")
            cursor.execute(f'UPDATE traders SET status = "block" WHERE trader_id = {trader_id}')
            conn.commit()
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Пользователь успешно заблокирован',
                                   reply_markup=kb_black_list)
        except ValueError as e:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Вы ввели не численное значение',
                                   reply_markup=kb_black_list)
            await state.reset_state()
            await state.finish()
        await state.reset_state()
        await state.finish()
    except KeyError as e:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Вы недавно добавляли этого пользователя в чс. Повторите попытку для подтверждения.',
                               reply_markup=kb_black_list)
        await state.reset_state()
        await state.finish()
    except sqlite3.IntegrityError as e:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Этот пользователь уже в черном списке.',
                               reply_markup=kb_black_list)
        await state.reset_state()
        await state.finish()
    


@dp.message_handler(state=Bl_Id_User.id)
async def add_user(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['id'] = message.text
    s = await state.get_data()
    try:
        trader_id = s['id']
        try:
            trader_id = int(trader_id)
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute(f"""INSERT INTO black_list VALUES ('{trader_id}', 'user');""")
            cursor.execute(f'UPDATE users SET status = "block" WHERE user_id = {trader_id}')
            conn.commit()
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Пользователь успешно заблокирован',
                                   reply_markup=kb_black_list)
        except ValueError as e:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Вы ввели не численное значение',
                                   reply_markup=kb_black_list)
            await state.reset_state()
            await state.finish()
        await state.reset_state()
        await state.finish()
    except KeyError as e:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Вы недавно добавляли этого пользователя в чс. Повторите попытку для подтверждения.',
                               reply_markup=kb_black_list)
        await state.reset_state()
        await state.finish()
    except sqlite3.IntegrityError as e:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Этот пользователь уже в черном списке.',
                               reply_markup=kb_black_list)
        await state.reset_state()
        await state.finish()


# Удаление
@dp.message_handler(state=UserDel.id)
async def set_api(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['id'] = message.text
    s = await state.get_data()
    try:
        user_id = s['id']
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            info = cursor.execute(f"""SELECT * FROM black_list WHERE id={user_id};""").fetchone()
            stat = cursor.execute(f'SELECT status FROM black_list WHERE id = {user_id}').fetchone()[0]
            if info is not None:
                cursor.execute(f"""DELETE FROM black_list WHERE id={user_id};""")
                if stat == 'user':
                    cursor.execute(f'UPDATE users SET status = "free" WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET api_key = "", api_secret = "" WHERE user_id = {user_id}')
                elif stat == 'trader':
                    cursor.execute(f'UPDATE traders SET status = "active" WHERE trader_id = {user_id}')
                    cursor.execute(f'UPDATE traders SET api_key = "", api_secret = "" WHERE trader_id = {user_id}')
                conn.commit()
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Пользователь успешно удален из чс.',
                                       reply_markup=kb_black_list)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Пользователь не найден в чс.',
                                       reply_markup=kb_black_list)
            await state.reset_state()
            await state.finish()
        except ValueError as e:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Вы ввели не численное значение',
                                   reply_markup=kb_black_list)
            await state.reset_state()
            await state.finish()
        await state.reset_state()
        await state.finish()
    except KeyError as e:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Вы только что добавили этого пользователя. Повторите попытку для подтверждения.',
                               reply_markup=kb_black_list)
        await state.reset_state()
        await state.finish()
        

async def set_user_status(conn,id,status):
    cursor = conn.cursor()
    try:
        cursor.execute(f'UPDATE users SET status = "{status}" WHERE user_id = {int(id)}')
    except:
        return False
    if status == 'paid':
        conn.commit()
        conn.close()
    return True


async def set_trader_status(conn, id, status):
    cursor = conn.cursor()
    try:
        data = cursor.execute(f"SELECT api_key, api_secret FROM users WHERE user_id = {id}").fetchone()
        cursor.execute(f'DELETE FROM users WHERE user_id = {id}')
        if data[0] != '' and data[1] != '':
            cursor.execute(f"""INSERT INTO traders (trader_id, api_key, api_secret, subscribers, history, trader_keys, 
status, name) VALUES ({id}, ?, ?, ?, ?, ?, 'trader', ?)""", (data[0], data[1], None, None, None, None))
        else:
            cursor.execute(f"INSERT INTO traders (trader_id, api_key, api_secret, subscribers, history, trader_keys,"
                           f"status, name) VALUES ({id}, ?, ?, ?, ?, ?, 'trader', ?)", (None, None, None, None, None, None))
    except Exception as e:
        print(e)
        return False
    if status == 'trader':
        conn.commit()
        conn.close()
    return True
