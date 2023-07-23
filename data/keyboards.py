from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# КНОПКИ И ДЛЯ ПЛАТНОГО ЮЗЕРА И ДЛЯ ТРЕЙДЕРА
b_edit_api = KeyboardButton('Редактировать API')

# Бесплатная Клавиатура
kb_free = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("Описание")
b2 = KeyboardButton('Наши Трейдеры')
b3 = KeyboardButton("Инструкция")
b4 = KeyboardButton("Оформить подписку")
b5 = KeyboardButton('Информация')
kb_free.add(b1,b3).add(b2, b5).add(b4)

# Платная Клавиатура (Незареганный аккаунт)
kb_unreg = ReplyKeyboardMarkup(resize_keyboard=True)
b_unreg1 = KeyboardButton("Авторизация")
kb_unreg.add(b_unreg1).add(b3)

# Платная Клавиатура (Зареганный аккаунт)
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)
b_profile = KeyboardButton("Профиль")
b_settings = KeyboardButton("Настройки бота")
b_subscr = KeyboardButton("Подписка на трейдера")
b_info = KeyboardButton("Информация")
b_start = KeyboardButton("Начать торговлю")
# b_edit_api = KeyboardButton('Редактировать API')
# b_leverage = KeyboardButton('Кредитное плечо')
kb_reg.add(b_profile,b_settings).add(b_subscr,b_info).add(b_start)


# Клавиатура профиля
kb_prof = ReplyKeyboardMarkup(resize_keyboard=True)
prof_b1 = KeyboardButton("Баланс")
prof_b2 = KeyboardButton("Статистика")
prof_b3 = KeyboardButton("Подписка")
b_all_trader_sub = KeyboardButton('Мои трейдеры')
prof_b4 = KeyboardButton("Назад")
kb_prof.add(prof_b1, prof_b2).add(prof_b3, b_all_trader_sub).add(prof_b4)

# Клавиатура настройки бота
kb_settings = ReplyKeyboardMarkup(resize_keyboard=True)
set_b1 = KeyboardButton("Сумма сделки")
set_b2 = KeyboardButton("Управление плечом")
kb_settings.add(set_b1).add(set_b2).add(prof_b4)

# Клавиатура подписки на трейдера
kb_subscribe_on_trader = ReplyKeyboardMarkup(resize_keyboard=True)
sb1 = KeyboardButton("Подписаться на трейдера")
sb2 = KeyboardButton("Отписаться от трейдера")
sb3 = KeyboardButton("Назад")
kb_subscribe_on_trader.add(sb1).add(sb2).add(sb3)

# Клавиатура подтверждения отписки
kb_confirmation = ReplyKeyboardMarkup(resize_keyboard=True)
сb1 = KeyboardButton("ДА")
сb2 = KeyboardButton("НЕТ")
cb3 = KeyboardButton("Назад в меню подписки")
kb_confirmation.add(сb1, сb2).add(cb3)

# Клавиатура плеча
kb_leverage = ReplyKeyboardMarkup(resize_keyboard=True)
lb1 = KeyboardButton("Максимальное плечо монеты")
lb2 = KeyboardButton('Установить плечо')
kb_leverage.add(lb1,lb2).add(prof_b4)


# Клава установки плеча
kb_set_leverage = ReplyKeyboardMarkup(resize_keyboard=True)
kb_set_leverage1 = KeyboardButton('Сбросить плечо')
kb_set_leverage2 = KeyboardButton('Изменить')
kb_set_leverage3 = KeyboardButton('Установить плечо как у трейдера')
kb_set_leverage.add(kb_set_leverage1, kb_set_leverage2).add(kb_set_leverage3).add(prof_b4)


kb_inform = ReplyKeyboardMarkup(resize_keyboard=True)
info_b1 = KeyboardButton("О нас")
info_b2 = KeyboardButton("Инструкция")
info_b3 = KeyboardButton("Наши трейдеры")
info_b4 = KeyboardButton("Пользовательское соглашение")
kb_inform.add(info_b1, info_b2).add(info_b3).add(info_b4).add(sb3)

# Клавиатура вида контракта
kb_contract = ReplyKeyboardMarkup(resize_keyboard=True)
conb1 = KeyboardButton("Линейный")
conb2 = KeyboardButton("Обратный")
conb3 = KeyboardButton("Назад в меню плеча")
kb_contract.add(conb1).add(conb2).add(conb3)

# Клавиатура инструкции
kb_instruct = ReplyKeyboardMarkup(resize_keyboard=True)
b_ins1 = KeyboardButton("Как создать API ключ?")
b_ins2 = KeyboardButton("❌Предостережения❌")
kb_instruct.add(b_ins1).add(b_ins2).add(prof_b2)

# Клавиатура админ панели
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
adb1 = KeyboardButton('Статистика бота')
adb2 = KeyboardButton('Цены')
adb3 = KeyboardButton('Черный список')
adb4 = KeyboardButton('Вывод данных о клиенте')
adb5 = KeyboardButton('Выдать статус')
adb6 = KeyboardButton('Перешифровка')
kb_admin.add(adb1, adb2).add(adb3, adb4).add(adb5, adb6)

# Клавиатура черного списка
kb_black_list = ReplyKeyboardMarkup(resize_keyboard=True)
bl_btn1 = KeyboardButton('Посмотреть заблокированных')
bl_btn2 = KeyboardButton('Добавить в чс')
bl_btn3 = KeyboardButton('Удалить из чс')
bl_btn4 = KeyboardButton('Назад в админку')
kb_black_list.add(bl_btn1).add(bl_btn2, bl_btn3).add(bl_btn4)

# Клавиатура трейдера
trade1 = KeyboardButton('Статистика Профиля')
trade2 = KeyboardButton('Ключи')
trade3 = KeyboardButton('Помощь')
trade4 = KeyboardButton('Вкл отслеживание')
trade5 = KeyboardButton('Выкл отслеживание')
kb_trader = ReplyKeyboardMarkup(resize_keyboard=True)
kb_trader.add(trade1, trade2).add(trade3, b_edit_api).add(trade4)
kb_trader2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_trader2.add(trade1, trade2).add(trade3, b_edit_api).add(trade5)


# Клавиатура статистики
kb_stat = ReplyKeyboardMarkup(resize_keyboard=True)
stat_b1 = KeyboardButton("Открытые сделки")
stat_b2 = KeyboardButton("Мои активы")
stat_b3 = KeyboardButton("Баланс")
stat_b4 = KeyboardButton("Профит/убыток")
kb_stat.add(stat_b1, stat_b2).add(stat_b3, stat_b4)


# Клавиатура ключей
kb_keys = ReplyKeyboardMarkup(resize_keyboard=True)
key1 = KeyboardButton('Создать ключ')
key2 = KeyboardButton('Удалить ключ')
key3 = KeyboardButton('Вывод всех ключей')
key4 = KeyboardButton('Вернуться')
kb_keys.add(key1, key2).add(key3).add(key4)

