import sqlite3

sqlite = sqlite3.connect('resource/database.db')
cursor = sqlite.cursor()


def can_level(num: int):
    """Проверяем, что уровень открыт"""
    response = cursor.execute("""SELECT * FROM levels""").fetchone()
    if response[num - 1] != 0:
        return True
    return False


def open_next_level():
    """Открываем следующий уровень"""
    global sqlite
    response = cursor.execute("""SELECT * FROM levels""").fetchone()
    if response[-1] == 1:
        return True

    get_num_to_open = response.index(0)
    cursor.execute(f"""UPDATE levels SET level{get_num_to_open + 1} = 1""").fetchone()
    sqlite.commit()
    return True