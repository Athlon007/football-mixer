from flask_restx import Api
from flask import Blueprint

from .main.controller.mixer_controller import api as mixer_ns
from .main.controller.system_controller import api as system_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus (restx) web service',
    security='apikey'
)

api.add_namespace(mixer_ns, path='/mixer')
api.add_namespace(system_ns, path='/system')
