from bson import ObjectId
from server import MONGO


def get_next_id(collection_name, session=None):
    """ Получить следующий ID """
    result = MONGO.db.counter.find_one_and_update(
        filter={"_id": collection_name},
        update={"$inc": {"count": 1}},
        upsert=True,
        new=True,
        session=session
    )
    return ObjectId(str(result["count"]).zfill(24))
