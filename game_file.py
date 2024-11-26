import json

FILE_NAME = "users_data.json"

def get_user_data(user_id):
    """
    Получить данные пользователя по его ID.
    Если данных нет, возвращается начальный баланс и игровая статистика.
    """
    try:
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if str(user_id) not in data:
        data[str(user_id)] = {"balance": 1000, "gameplay": 0}
        update_user_data(user_id, data[str(user_id)])

    return data[str(user_id)]

def update_user_data(user_id, user_data):
    """
    Обновить данные пользователя в файле.
    """
    try:
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[str(user_id)] = user_data

    with open(FILE_NAME, 'w') as file:
        json.dump(data, file, indent=4)
