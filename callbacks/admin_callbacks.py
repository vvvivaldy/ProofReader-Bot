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
            cursor.execute("SELECT date, user_id, amount, tranzaktion FROM purchase_history")
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