from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""ДЛЯ ОПЛАТЫ"""

#Клавиатура оплаты
paykb = InlineKeyboardMarkup(row_width=2)
payb1 = InlineKeyboardButton(text = '1 неделя', callback_data='1 неделю')
payb2 = InlineKeyboardButton(text = '1 месяц', callback_data='1 месяц')
payb3 = InlineKeyboardButton(text = '3 месяца', callback_data='3 месяца')
payb4 = InlineKeyboardButton(text = '6 месяцев', callback_data='6 месяцев')
payb5 = InlineKeyboardButton(text = '1 год', callback_data='1 год')
paykb.add(payb1, payb2).add(payb3, payb4).add(payb5)

"""ДЛЯ АДМИН ПАНЕЛИ"""
# СТАТИСТИКА
# основные кнопки
ikas = InlineKeyboardMarkup(row_width=1)
ibas1 = InlineKeyboardButton(text='Users and Traders',callback_data='uat')
ibas2 = InlineKeyboardButton(text='NEW users and Traders',callback_data= 'new')
ibas3 = InlineKeyboardButton(text='transactions',callback_data= 'trans')
ikas.add(ibas1,ibas2,ibas3)

# для ibas1


# для ibas3
