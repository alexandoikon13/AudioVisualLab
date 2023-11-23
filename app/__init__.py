from flask import Flask
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    # MongoDB setup
    mongo_uri = os.getenv('MONGO_URI')
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client.ClusterPortfolio
    app.db = db

    from .routes import init_routes
    init_routes(app)

    return app
