from flask import Flask
from flask_socketio import SocketIO

import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

from .config import config_by_name
from flask.app import Flask

from flask_cors import CORS

from app.main.service.model_service import load_ml_model

#print('Loading Model...')
#ml_model = load_model('models/mirphil_1000_1.0.h5')
#print('Model Loaded')

socketio = SocketIO()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__, static_url_path='/static')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Set maximum upload size to 100 MB
    CORS(app)

    config_file = config_by_name[config_name]

    app.config.from_object(config_file)

    socketio.init_app(app,
                      cors_allowed_origins=','.join(config_file.ALLOWED_HOSTS)
                      )

    return app