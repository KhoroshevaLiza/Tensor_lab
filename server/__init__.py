import os

from flask import Flask, jsonify
from flask_pymongo import PyMongo

from .utils.encoder import MongoJSONEncoder

APP = Flask(__name__, static_folder="../client")
APP.json_encoder = MongoJSONEncoder
APP.config["JSON_AS_ASCII"] = False
APP.config["MONGO_URI"] = "mongodb+srv://amd:admin14@sazhinmongodb-znyz8.mongodb.net/photorun?retryWrites=true&w=majority"
MONGO = PyMongo(APP)

from .db.database import create_collections

create_collections()

from .db.start_value_db import add_start_values

if os.environ.get("FLASK_ENV") == "development" or MONGO.db.posts.count_documents({}) == 0:
    add_start_values()

from . import views
from .api import feed_printer, post_operations, register_user
