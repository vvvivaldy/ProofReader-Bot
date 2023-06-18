from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




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
