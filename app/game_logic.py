import random

try:
    from app import db
except ImportError:
    db = None


def get_words_from_db():
    _dict = {}
    try:
        # Проверяем, что модуль базы загружен
        if db and hasattr(db, 'get_collection'):
            collection = db.get_collection()
            # Ошибка авторизации PyMongo происходит именно во время выполнения этого цикла,
            # поэтому блок try-except должен оборачивать его целиком
            for w in collection.find({"guessed_count": 0}):
                _dict[w["word"]] = w["hint"]

            # Если база подключилась, но пустая, переходим к заглушке
            if _dict:
                return _dict

    except Exception as e:
        # Пишем ошибку в консоль, чтобы вы её видели, но сервер НЕ падал
        print(f"\n[MongoDB Предупреждение]: Ошибка подключения/авторизации: {e}")
        print("[MongoDB Предупреждение]: Переключаюсь на локальную заглушку.\n")

    # Резервный словарь-заглушка (сработает, если упала авторизация MongoDB)
    return {
        "ЯКУБОВИЧ": "Бессменный ведущий капитал-шоу.",
        "БАРАБАН": "Предмет, который вращают участники в студии.",
        "МУЗЕЙ": "Место, куда отправляются все подарки от участников."
    }


def get_secret_and_mask(_dict):
    keys = list(_dict.keys())
    # Если база пуста или все слова угаданы, возвращаем дефолтное значение
    if not keys:
        return "ПОЛЕ", ['*'] * 4

    ind = random.randint(0, len(keys) - 1)
    secret = keys[ind]
    mask = ['*'] * len(secret)
    return secret, mask


def start_new_game(session):
    """Инициализирует новую игру и сохраняет состояние в сессию Flask"""
    _dict = get_words_from_db()
    secret, mask = get_secret_and_mask(_dict)

    session['secret'] = secret.upper()
    session['mask'] = mask
    session['hint'] = _dict.get(secret, "Описание отсутствует")


def process_letter(session, letter):
    """Проверяет букву и обновляет маску в сессии (исходная логика check_letter)"""
    secret = session.get('secret', '')
    mask = session.get('mask', [])

    if secret and letter:
        letter = letter.upper()
        for ind, val in enumerate(secret):
            if val.upper() == letter:
                mask[ind] = letter

        session['mask'] = mask
        session.modified = True
