from flask import jsonify, request
from server import APP, MONGO
from server.db.db_exception import ErrorDataDB
from server.utils.transaction import (commit_with_retry,
                                      run_transaction_with_retry)


@APP.route("/api/registration", methods=["POST"])
def register_new_user():
    """Регистрация пользователя"""
    try:
        data = request.get_json()
        check_request_dict(data)
        with MONGO.cx.start_session() as session:
            user_login = api_register_user(session, data)
    except ErrorDataDB as err:
        return jsonify({"message": err.message, "login": None, "is_success": False})
    return jsonify({"login": user_login, "is_success": True})


def check_request_dict(data):
    """ Проверить тип входных данных, требуется словарь """
    if not isinstance(data, dict):
        raise ErrorDataDB(
            "В запросе не передан словарь. Передан {}".format(
                type(data))
        )


@run_transaction_with_retry
def api_register_user(session, data):
    """ Добавить нового пользователя"""
    if not check_login(data["login"]):
        raise ErrorDataDB("Такой пользователь уже зарегистрирован")
    try:
        user = {
            "login": data["login"],
            "password": data["password"]
        }
    except KeyError as ex:
        raise ErrorDataDB("Отсутствует ключ {}".format(ex))
    MONGO.db.users.insert_one(user, session=session)
    commit_with_retry(session)
    return data["login"]


def check_login(login_f):
    """Поиск по базе такого же логина """
    a = MONGO.db.users.find(
        {"login": login_f},
        {
            "_id": 0,
            "login": 1,
            "password": 0
        }
    )
    if a.count() == 0:
        return True
    return False
