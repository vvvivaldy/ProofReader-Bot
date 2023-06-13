from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Бесплатная Клавиатура
kb_free = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("Описание")
b3 = KeyboardButton("Инструкция")
b4 = KeyboardButton("Оформить подписку")
kb_free.add(b1).add(b3).add(b4)

# Платная Клавиатура (Незареганный аккаунт)
kb_unreg = ReplyKeyboardMarkup(resize_keyboard=True)
b_unreg1 = KeyboardButton("Авторизация")
kb_unreg.add(b_unreg1)

# Платная Клавиатура (Зареганный аккаунт)
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)
b_p1 = KeyboardButton("Профиль")
b_p2 = KeyboardButton("Настройки бота")
b_p4 = KeyboardButton("Начать торговлю")
kb_reg.add(b_p1).add(b_p2).add(b3).add(b_p4)

# Клавиатура профиля
kb_profile = ReplyKeyboardMarkup(resize_keyboard=True)
prof_b1 = KeyboardButton("Баланс")
prof_b2 = KeyboardButton("В меню")
kb_profile.add(prof_b1).add(prof_b2)

# Инлайн клавиатура инструкции
kb_instruct = ReplyKeyboardMarkup(resize_keyboard=True)
b_ins1 = "Как начать пользоваться ботом?"
b_ins2 = "❌Предостережения❌"
kb_instruct.add(b_ins1).add(b_ins2).add(prof_b2)
