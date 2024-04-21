from flask import request
from flask_restx import Resource, Namespace

from typing import Dict, Tuple

api = Namespace('mixer', description='mixer related operations')

@api.route('/status')
class SystemStatus(Resource):
    """
        System Status Resource
    """
    @api.doc('get system status')
    def get(self) -> Tuple[Dict[str, str], int]:
        return {'status': 'up'}, 200