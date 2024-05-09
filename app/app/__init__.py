from flask_restx import Api
from flask import Blueprint
# and now the socketio import

from .main.controller.mixer_controller import api as mixer_ns
from .main.controller.system_controller import api as system_ns
from .main.controller.predict_controller import api as predict_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Foodball Mixer API',
    version='1.0',
    description='AI-powered foodball mixer API',
    security='apikey'
)

api.add_namespace(mixer_ns, path='/mixer')
api.add_namespace(system_ns, path='/system')
api.add_namespace(predict_ns)
