from flask import Flask
from flask_socketio import SocketIO

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, Sequential

from .config import config_by_name
from flask.app import Flask

from flask_cors import CORS

print('Loading Model...')
ml_model = load_model('model.h5')
print('Model Loaded')

socketio = SocketIO()

def create_app(config_name: str) -> Flask:
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    app.config.from_object(config_by_name[config_name])

    socketio.init_app(app)

    return app