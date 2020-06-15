""" Парсеры """
from bson import ObjectId, errors

from server.db.db_exception import ErrorDataDB


def parse_object_id(str_id):
    """ Преобразовать id в ObjectId """
    try:
        return ObjectId(str_id)
    except errors.InvalidId:
        raise ErrorDataDB("Некорректный id объекта: {}".format(str_id))

