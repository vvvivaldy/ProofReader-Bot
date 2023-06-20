from handlers.A_head_of_handlers import *

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
            pass

        case 'trans':
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT date, user_id, amount, transaction FROM purchase_history")
            result = cursor.fetchall()
            for i in range(len(result)):
                date2 = result[i][0]
                user_id2 = result[i][1]
                amount2 = result[i][2]
                tranzaktion = result[i][3]
                text2 = f'<b>Дата:</b> {date2}\n<b>Айди:</b> {user_id2}\n<b>Количество:</b> {amount2}\n<b>Номер транзакции:</b> {tranzaktion}\n\n\n'
                await bot.send_message(chat_id=callback.from_user.id, text=text2, parse_mode="HTML")

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



@dp.message_handler(state=Bl_Id_Trader.id)
async def add_trader(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['id'] = message.text
        await state.finish()
    s = await state.get_data()
    trader_id = s['id']
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO black_list VALUES ('{trader_id}', 'trader');""")
    conn.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Пользователь успешно заблокирован',
                           reply_markup=kb_black_list)


@dp.message_handler(state=Bl_Id_User.id)
async def add_user(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['id'] = message.text
        await state.finish()
    s = await state.get_data()
    trader_id = s['id']
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO black_list VALUES ('{trader_id}', 'user');""")
    conn.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Пользователь успешно заблокирован',
                           reply_markup=kb_black_list)


# Удаление
@dp.message_handler(state=UserDel.id)
async def set_api(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['id'] = message.text
        await state.finish()
    s = await state.get_data()
    user_id = s['id']
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    info = cursor.execute(f"""SELECT * FROM black_list WHERE id={user_id};""").fetchone()
    if info is not None:
        cursor.execute(f"""DELETE FROM black_list WHERE id={user_id};""")
        conn.commit()
        await bot.send_message(chat_id=message.from_user.id,
                               text='Пользователь успешно удален из чс.',
                               reply_markup=kb_black_list)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Пользователь не найден в чс.',
                               reply_markup=kb_black_list)
