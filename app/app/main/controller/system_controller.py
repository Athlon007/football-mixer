from flask_restx import Resource, Namespace

from typing import Dict, Tuple

api = Namespace('status', description='system status operations')


@api.route('/check')
class SystemStatus(Resource):
    """
        System Status Resource
    """
    @api.doc('get system status')
    def get(self) -> Tuple[Dict[str, str], int]:
        return {'status': 'up'}, 200
