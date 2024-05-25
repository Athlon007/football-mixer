from flask import Flask
from flask_socketio import SocketIO

import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

from .config import config_by_name
from flask.app import Flask

from flask_cors import CORS

print('Loading Model...')
ml_model = load_model('mirphil_v1.h5')
print('Model Loaded')

socketio = SocketIO()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__, static_url_path='/static')
    CORS(app)

    config_file = config_by_name[config_name]

    app.config.from_object(config_file)

    socketio.init_app(app,
                      cors_allowed_origins=','.join(config_file.ALLOWED_HOSTS)
                      )

    return app