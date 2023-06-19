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


# Добавление
@dp.callback_query_handler(text="Trader")
async def trader_callbacks(callback: types.CallbackQuery):
    await callback.message.answer(text="Введите id трейдера")
    await Bl_Id_Trader.id.set()


@dp.callback_query_handler(text="User")
async def user_callbacks(callback: types.CallbackQuery):
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
