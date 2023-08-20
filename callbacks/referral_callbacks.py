from handlers.A_head_of_handlers import *


@dp.callback_query_handler(lambda c: c.data[0] == 'R')
async def referral_callback(callback: types.CallbackQuery):
    callback.data = callback.data[1:]
    if callback.data == 'get_partnership':
        conn, cursor = db_connect()
        cursor.execute(f'UPDATE referral SET status = "on" WHERE id = {callback.from_user.id}')
        conn.commit()
        await callback.answer(text='Поздравляем! Вы стали партнером🤑')

        await bot.delete_message(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id)
        
        salary = int(cursor.execute(f'SELECT salary FROM referral WHERE id = {callback.from_user.id}').fetchone()[0])
        sale = int(cursor.execute(f'SELECT sale FROM referral WHERE id = {callback.from_user.id}').fetchone()[0])
        await bot.send_photo(chat_id=callback.from_user.id,
                                    photo='https://avatars.mds.yandex.net/i?id=409af83d0551ff3d1939e278fb3a0debe6f6883f-9291097-images-thumbs&n=13',
                                    caption=f'Партнёрская программа ProofReader\n\n\n'
                                    f'Ваша ссылка для партнёрской программы: \n<b>*не настроено*</b>\n\n'
                                    f'По ней приведенные вами клиенты будут покупать подписку, а часть стоимости придет на ваш счет: \n<b>*не настроено*</b>\n\n'
                                    f'Ваша прибыль с каждой покупки (скидка не влияет на прибыль) = <b>{salary}%</b>\n\n'
                                    f'Для клиентов по вашей ссылке скидка <b>{sale}%</b>',
                                    reply_markup=kb_ref,
                                    parse_mode='html')
        
    elif callback.data == 'get_partnership_info':
        await bot.send_message(chat_id = callback.from_user.id,
                               text=REFERRAL)
        
    elif callback.data == "url":
        await bot.send_message(chat_id = callback.from_user.id,
                               text="Тут будет ф-ция смены url")
        
    elif callback.data == 'bank':
        await bot.send_message(chat_id = callback.from_user.id,
                               text="Тут будет ф-ция смены счёта")
        