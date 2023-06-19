from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""ДЛЯ ОПЛАТЫ"""

#Клавиатура оплаты
paykb = InlineKeyboardMarkup(row_width=2)
payb1 = InlineKeyboardButton(text = '1 неделя', callback_data='P1 неделю')
payb2 = InlineKeyboardButton(text = '1 месяц', callback_data='P1 месяц')
payb3 = InlineKeyboardButton(text = '3 месяца', callback_data='P3 месяца')
payb4 = InlineKeyboardButton(text = '6 месяцев', callback_data='P6 месяцев')
payb5 = InlineKeyboardButton(text = '1 год', callback_data='P1 год')
paykb.add(payb1, payb2).add(payb3, payb4).add(payb5)

"""ДЛЯ АДМИН ПАНЕЛИ"""
# СТАТИСТИКА
# основные кнопки
ikas = InlineKeyboardMarkup(row_width=1)
ibas1 = InlineKeyboardButton(text='Users and Traders',callback_data='Auat')
ibas2 = InlineKeyboardButton(text='NEW users and Traders',callback_data= 'Anew')
ibas3 = InlineKeyboardButton(text='transactions',callback_data= 'Atrans')
ikas.add(ibas1,ibas2,ibas3)

# для ibas1


# для ibas3

#ЦЕНЫ
inl_kb_pr = InlineKeyboardMarkup(row_width=2)
ikp1 = InlineKeyboardButton(text='Назад', callback_data='Areturn')
ikp2 = InlineKeyboardButton(text='Изменить', callback_data='Aedit')
inl_kb_pr.add(ikp1,ikp2)