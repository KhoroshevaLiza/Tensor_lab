from pymongo.write_concern import WriteConcern
from server import MONGO


def create_collections():
    """ Создать коллекции БД """
    wc_majority = WriteConcern(w="majority", wtimeout=1000)
    collections = ["posts", "users"]
    for collection in collections:
        if not collection in MONGO.db.collection_names():
            MONGO.db.create_collection(collection, write_concern=wc_majority)
