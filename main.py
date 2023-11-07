from handlers.F_tail_of_handlers import *


# Успешный запуск бота
async def on_startup(_):
    print("Я был запущен")


# Запуск ботач
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)