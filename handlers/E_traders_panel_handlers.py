from handlers.D_paid_function_handlers import *

# проверка на трейдера
def trader_validate(id: int) -> bool:
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()
    try:
        res = cursor.execute(f'SELECT status FROM traders WHERE trader_id={id};').fetchone()[0]
        if res == 'НАДО НАПИСАТЬ КАКОЙ СТАТУС У ТРЕЙДЕРА':
            return True
        else:
            return False
    except:
        return False
