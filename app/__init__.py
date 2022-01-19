from flask import Flask
import pymongo
import os

from app import routes as posts_view

DB = os.getenv('DATABASE')

client = pymongo.MongoClient(DB)
db = client['kenzie']
collection = db['posts']

def create_app():

    app = Flask(__name__, static_folder=None)
    posts_view.init_app(app)

    return app