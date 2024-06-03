from flask_restx import Resource, Namespace

from typing import Dict, Tuple

api = Namespace('models', description='model related operations')


@api.route('/')
class ModelsList(Resource):
    """
        Returns a list of models available in the system
    """
    @api.doc('get system status')
    def get(self) -> Tuple[Dict[str, str], int]:
        return {'status': 'up'}, 200