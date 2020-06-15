""" Страницы приложения """
from flask import send_from_directory

from . import APP


@APP.route("/")
@APP.route("/index")
@APP.route("/feed")
def index():
    """ Главная страница """
    return send_from_directory(APP.static_folder, 'index.html')


@APP.route("/upload")
def events_list():
    """ Страница загрузки фотографии POST """
    return send_from_directory(APP.static_folder, 'upload.html')


@APP.route("/register")
def booking():
    """ Страница регистрации POST """
    return send_from_directory(APP.static_folder, 'register.html')


