"""
This module contains the service functions for the ML models.
"""
import os
import json
from keras.models import load_model

ml_model = None
ml_model_name = None

def load_ml_model(model_name):
    """
    Load the ML model from the file system.
    """

    path = 'models/' + model_name + '.h5'

    if not os.path.exists(path):
        return {'status': 'model not found'}, 404

    print('Loading Model...')

    global ml_model
    global ml_model_name
    ml_model = load_model(path)
    ml_model_name = model_name

    print('Model ' + model_name + ' Loaded!')

    return { 'status': 'model loaded', 'model': model_name }, 200

def list_models():
    """
    Returns a list of models available in the system
    """
    if not os.path.exists('models/meta.json'):
        return {'status': 'no models found'}, 404

    # Load the 'meta.json' for the list of models
    global ml_model_name
    models = json.load(open('models/meta.json', 'r', encoding='utf-8'))
    return { 'current_model': ml_model_name, 'models': models}, 200

# init default model to be used
load_ml_model('mirphil_1000_1.0')
