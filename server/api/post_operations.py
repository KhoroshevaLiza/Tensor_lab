""" Операции с публикациями """
from flask import jsonify, request
from server import APP, MONGO
from server.db import counter_id, check_password
from server.db.db_exception import ErrorDataDB
from server.utils.parsers import parse_object_id
from urllib import request
from datetime import datetime, timedelta
from server.utils.transaction import (commit_with_retry,
                                      run_transaction_with_retry)


@APP.route("/api/deletepost", methods=["POST"])
def delete_post():
    """ Удаление записи """
    try:
        data = request.get_json()
        post_id, login, password = parse_data(data)
        check_password.check_password(login, password)
        check_owner(post_id, login)
        with MONGO.cx.start_session() as session:
            txn_delete_post(session, post_id)
    except ErrorDataDB as error_db:
        return jsonify({"message": error_db.message, "is_success": False})
    return jsonify({"is_success": True})


def check_request_dict(data):
    """ Проверить тип входных данных, должен быть словарь """
    if not isinstance(data, dict):
        raise ErrorDataDB(
            "В запросе должен быть передан словарь. Передан {}".format(
                type(data))
        )


def check_owner(post_id, login_f):
    """ Проверка, владеет ли данным постом данный логин """
    a = MONGO.db.posts.find(
        {"_id": post_id},
        {
            "_id": 0,
            "name": 0,
            "text": 0,
            "theme_name": 0,
            "photo": 0,
            "author": 1,
            "publish_time": 0
        }
    )
    if a.count() == 0:
        return False
    if a.get("author") == login_f:
        return True
    return False


def parse_data(data):
    """ Разбиваем полученные данные """
    try:
        check_request_dict(data)
        post_id = parse_object_id(data["id"])
        login = data["login"]
        password = data["password"]
    except KeyError as key_error:
        raise ErrorDataDB("Отсутствует ключ {}".format(key_error))
    return post_id, login, password


@run_transaction_with_retry
def txn_delete_post(session, post_id):
    """Удалить публикацию"""
    MONGO.db.booking.delete_one({"_id": post_id})
    commit_with_retry(session)
    return True


@APP.route("/api/addpost", methods=["POST"])
def add_post():
    """Создание новой публикации"""
    try:
        data = request.get_json()
        #login - и есть author поста
        name, text, theme, photo, login, password = parse_data_upload(data)
        time_now = datetime.utcnow() + timedelta(hours=3)
        if not is_valid(photo):
            raise ErrorDataDB("Ссылка на фотографию некорректная")
        check_password.check_password(login, password)
        post = {
            "_id": counter_id.get_next_id("posts"),
            "name": name,
            "text": text,
            "theme_name": theme,
            "photo": photo,
            "author": login,
            "publish_time": time_now
        }
        with MONGO.cx.start_session() as session:
            txn_add_post(session, post)
    except ErrorDataDB as error_db:
        return jsonify({"message": error_db.message, "is_success": False})
    return jsonify({"is_success": True})


def is_valid(url):
    try:
        request.urlopen(url)
        return True
    except:
        return False


def parse_data_upload(data):
    """ Разбиваем полученные данные """
    try:
        check_request_dict(data)
        name = data["name"]
        text = data["text"]
        theme = data["theme"]
        photo = data["photo"]
        login = data["login"]
        password = data["password"]
    except KeyError as key_error:
        raise ErrorDataDB("Отсутствует key {}".format(key_error))
    return name, text, theme, photo, login, password


@run_transaction_with_retry
def txn_add_post(session, post):
    """ Добавить публикацию """
    MONGO.db.posts.insert_one(post)
    commit_with_retry(session)
    return True
