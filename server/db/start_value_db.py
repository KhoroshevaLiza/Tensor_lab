"""Первичное заполнение данных БД"""
from datetime import datetime
from server import MONGO
from . import counter_id


def add_start_values():
    add_users()
    add_start_posts()


def add_users():
    user1 = {
        "login": "admin",
        "password": ""
    }
    MONGO.db.users.insert_one(user1)


def add_start_posts():
    add_post_1()
    add_post_2()
    add_post_3()


def add_post_1():
    post1 = {
        "_id": counter_id.get_next_id("posts"),
        "name": "Виталик",
        "text": "Виталик-студент",
        "theme_name": "Студенчество Виталика",
        "photo": "1.jpg",
        "author": "admin",
        "publish_time": datetime.fromisoformat("2017-04-02 17:00:00")
    }
    MONGO.db.posts.insert_one(post1)


def add_post_2():
    post2 = {
        "_id": counter_id.get_next_id("posts"),
        "name": "Виталик-2",
        "text": "Виталик-студент",
        "theme_name": "Студенчество Виталика",
        "photo": "2.jpg",
        "author": "admin",
        "publish_time": datetime.fromisoformat("2019-01-25 23:00:00")
    }
    MONGO.db.posts.insert_one(post2)


def add_post_3():
    post3 = {
        "_id": counter_id.get_next_id("posts"),
        "name": "Виталик-3",
        "text": "На взлёт",
        "theme_name": "Студенчество Виталика",
        "photo": "3.jpg",
        "author": "admin",
        "publish_time": datetime.fromisoformat("2016-02-13 13:00:00")
    }
    MONGO.db.posts.insert_one(post3)