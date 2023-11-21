from flask import Flask
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    # Directory where uploaded files will be stored
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # MongoDB setup
    mongo_client = MongoClient('mongodb://localhost:27017/')  # Update with your URI
    db = mongo_client.Cluster0
    app.db = db

    from .routes import init_routes
    init_routes(app)

    return app
