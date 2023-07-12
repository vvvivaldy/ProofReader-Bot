from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""ОБЩИЕ ДЛЯ ПЛАТНЫХ И ТРЕЙДЕРОВ"""
ik_edit_api = InlineKeyboardMarkup(row_width=1)
ib_edit_api = InlineKeyboardButton(text='Редактировать', callback_data='Dedit_api')
ik_edit_api.add(ib_edit_api)
# бработка калбэка будет в paid_callbacks.py


"""ДЛЯ ОПЛАТЫ"""
#Клавиатура оплаты
paykb = InlineKeyboardMarkup(row_width=2)
payb1 = InlineKeyboardButton(text = '1 неделя', callback_data='B1 неделю')
payb2 = InlineKeyboardButton(text = '1 месяц', callback_data='B1 месяц')
payb3 = InlineKeyboardButton(text = '3 месяца', callback_data='B3 месяца')
payb4 = InlineKeyboardButton(text = '6 месяцев', callback_data='B6 месяцев')
payb5 = InlineKeyboardButton(text = '1 год', callback_data='B1 год')
paykb.add(payb1, payb2).add(payb3, payb4).add(payb5)

"""ДЛЯ АДМИН ПАНЕЛИ"""
# СТАТИСТИКА
# основные кнопки
ikas = InlineKeyboardMarkup(row_width=1)
ibas1 = InlineKeyboardButton(text='Users and Traders',callback_data='Cuat')
ibas2 = InlineKeyboardButton(text='NEW users and Traders',callback_data= 'Cnew')
ibas3 = InlineKeyboardButton(text='transactions',callback_data= 'Ctrans')
ikas.add(ibas1,ibas2,ibas3)

# ВЫВОД ИНФЫ ОБ КЛИЕНТЕ
ikk = InlineKeyboardMarkup(row_width=2)
ikkb1 = InlineKeyboardButton(text='Пользователь', callback_data='Cuser_status')
ikkb2 = InlineKeyboardButton(text='Трейдер', callback_data='Ctrader_status')
ikk.add(ikkb1,ikkb2)

# ВЫДАЧА СТАТУСА
ikst = InlineKeyboardMarkup(row_width=2)
a = InlineKeyboardButton(text='set free', callback_data=f'Cset_free')
b = InlineKeyboardButton(text='set paid', callback_data=f'Cset_paid')
c = InlineKeyboardButton(text='Вернуться назад', callback_data='Creturn')
d = InlineKeyboardButton(text='set trader', callback_data='Cset_trader')
ikst.add(a,b, d, c)

# Выбор Период
ikb_period = InlineKeyboardMarkup(row_width=2)
q = InlineKeyboardButton(text='day', callback_data=f'Cday')
w = InlineKeyboardButton(text='week', callback_data=f'Cweek')
e = InlineKeyboardButton(text='month', callback_data='Cmonth')
r = InlineKeyboardButton(text='year', callback_data='Cyear')
ikb_period.add(q, w).add(e, r)

#ЦЕНЫ
inl_kb_pr = InlineKeyboardMarkup(row_width=2)
ikp1 = InlineKeyboardButton(text='Назад', callback_data='Creturn')
ikp2 = InlineKeyboardButton(text='Изменить', callback_data='Cedit')
inl_kb_pr.add(ikp1,ikp2)

inl_kb_status = InlineKeyboardMarkup(row_width=2)
ikbtn1 = InlineKeyboardButton(text='Трейдер', callback_data='CTrader')
ikbtn2 = InlineKeyboardButton(text='Юзер', callback_data='CUser')
inl_kb_status.add(ikbtn1, ikbtn2)

ikb_quantity = InlineKeyboardMarkup(row_width=2)
infinity = InlineKeyboardButton(text='Бесконечное', callback_data='Einfinity')
personal = InlineKeyboardButton(text='Персональное', callback_data='Epersonal')
ikb_quantity.add(infinity).add(personal)

# Трейдер статистика
ikb_trader_stat = InlineKeyboardMarkup(row_width=1)
itsb1 = InlineKeyboardButton(text='Подписано людей',callback_data='Epeople')
itsb2 = InlineKeyboardButton(text='Открытые сделки', callback_data='EOpenOrders')
itsb3 = InlineKeyboardButton(text='История сделок',callback_data='EHistoryOrders')
ikb_trader_stat.add(itsb1,itsb2,itsb3)


kb_order = InlineKeyboardMarkup(row_width=2)
k1 = InlineKeyboardButton(text='Отправить', callback_data='EpushOrder')
k2 = InlineKeyboardButton(text='Отмена', callback_data='EcancelOrder')
kb_order.add(k1).add(k2)
