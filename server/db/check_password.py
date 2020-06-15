from server import MONGO


def check_password(login_f, password):
    """Поиск по базе логина такого же, взятие пароля и сравнение"""
    a = MONGO.db.users.find(
        {"login": login_f},
        {
            "_id": 0,
            "login": 0,
            "password": 1
        }
    )
    if a.count() == 0:
        return False
    if a.get("password") == password:
        return True
    return False

