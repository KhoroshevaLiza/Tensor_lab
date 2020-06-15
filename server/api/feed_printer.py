from flask import jsonify, request

from server import APP, MONGO
from server.db.db_exception import ErrorDataDB


@APP.route("/api/get_full_feed", methods=["GET"])
def get_full_feed():
    """ Получить список всех публикаций """
    cursor = MONGO.db.posts.find(
        {},
        {
            "_id": 1,
            "name": 1,
            "text": 1,
            "theme_name": 1,
            "photo": 1,
            "author": 1,
            "publish_time": 1
        }
    ).sort("publish_time")
    posts = list(cursor)
    for post in posts:
        post["id"] = post.pop("_id")
    return jsonify({"posts_list": posts})


@APP.route("/api/get_theme_feed", methods=["GET"])
def get_theme_feed():
    """ Получить список всех публикаций по заданной теме """
    theme = request.args.get("theme")
    cursor = MONGO.db.posts.find(
        {
            "theme_name": theme
        },
        {
            "_id": 1,
            "name": 1,
            "text": 1,
            "theme_name": 1,
            "photo": 1,
            "author": 1,
            "publish_time": 1
        }
    ).sort("publish_time")
    posts = list(cursor)
    for post in posts:
        post["id"] = post.pop("_id")
    return jsonify({"posts_list": posts})


@APP.route("/api/get_author_feed", methods=["GET"])
def get_author_feed():
    """ Получить список всех публикаций автора """
    author = request.args.get("author")
    cursor = MONGO.db.posts.find(
        {
            "author": author
        },
        {
            "_id": 1,
            "name": 1,
            "text": 1,
            "theme_name": 1,
            "photo": 1,
            "author": 1,
            "publish_time": 1
        }
    ).sort("publish_time")
    posts = list(cursor)
    for post in posts:
        post["id"] = post.pop("_id")
    return jsonify({"posts_list": posts})
