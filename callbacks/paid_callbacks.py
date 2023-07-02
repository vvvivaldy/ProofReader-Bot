from handlers.A_head_of_handlers import *



@dp.callback_query_handler(lambda d: d.data[0] == 'D')
async def paid_callback(callback: types.CallbackQuery):
    callback.data = callback.data[1:]
    match callback.data:
        case 'edit_api':
            if paid_validate(callback.from_user.id):
                conn, cursor = db_connect()
                cursor.execute("SELECT status FROM users WHERE user_id = ?", (callback.from_user.id,))
                result = cursor.fetchone()
                if result[0] == "paid":
                    await bot.send_message(chat_id=callback.from_user.id,
                                        text="Введите ваш <b>api_key</b> и <b>api_secret</b> через пробел: ",
                                        parse_mode="HTML")
                    await EditApi.api.set()
                else:
                    await bot.send_message(chat_id=callback.from_user.id,
                                        text="Вы еще не оплатили подписку",
                                        parse_mode="HTML")
                    
            elif trader_validate(callback.from_user.id):
                conn, cursor = db_connect()
                cursor.execute("SELECT status FROM traders WHERE trader_id = ?", (callback.from_user.id,))
                result = cursor.fetchone()
                if result[0] == "trader":
                    global stream_websockets
                    if f'stream_{callback.from_user.id}' in stream_websockets: 
                        await callback.answer(text="💥Сначала выключите отслеживание ордеров!")
                    else:
                        await bot.send_message(chat_id=callback.from_user.id,
                                            text="Введите ваш <b>api_key</b> и <b>api_secret</b> через пробел: ",
                                            parse_mode="HTML")
                        await EditApiTrader.api.set()
                else:
                    await bot.send_message(chat_id=callback.from_user.id,
                                        text="У вас нет статуса трейдера",
                                        parse_mode="HTML")
            else: 
                await bot.send_message(chat_id=callback.from_user.id,
                                text="Мы не предусмотрели данный запрос. Повторите попытку.")
                

@dp.message_handler(state=(EditApi.api, EditApiTrader.api))
async def set_api(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['api'] = message.text
        client_type = proxy._state.split(':')[0]
    s = await state.get_data()

    if (await state.get_state()).split(':')[0] == 'EditApi': kb = kb_reg
    else : kb = kb_trader


    try:
        api_key = encrypt_api(s['api'].partition(' ')[0])
        api_secret = encrypt_api(s['api'].partition(' ')[2])
    except KeyError:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Что-то пошло не так, ключи не обновились. Попробуйте снова')
        await state.reset_state()
        await state.finish()
        return
    try:
        test = HTTP(
            api_key=decrypt_api(api_key),
            api_secret=decrypt_api(api_secret))
        test.get_account_info()
    except:
        await bot.send_message(message.chat.id, 'Api key или Api secret указаны неверно. Повторите попытку', reply_markup=kb)
        await state.reset_state()
        await state.finish()
        return
    
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    if client_type == 'EditApi':
        cursor.execute(f"""UPDATE users SET api_secret = "{api_secret}", api_key = "{api_key}"
                            WHERE user_id = {message.from_user.id}""")
    elif client_type == 'EditApiTrader':
        cursor.execute(f"""UPDATE traders SET api_secret = "{api_secret}", api_key = "{api_key}"
                            WHERE trader_id = {message.from_user.id}""")
    else:
        print('ЧТО_ТО ПОШЛО НЕ ТАК, ЭТОТ ОБРАБОТЧИК ПРИНИМАЕТ НЕ ТОЛЬКО EditApi и EditApiTrader!!!')
    conn.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Ваши API изменены', reply_markup=kb)
    await state.reset_state()
    await state.finish()



