from flask import request
from flask_restx import Resource, Namespace

from .. import socketio

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


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    msg = message[::-1]
    socketio.emit('message_response', {
        'response': msg
        })

@api.route('/')
class SocketIODocs(Resource):
    def get(self):
        """
        Documentation for SocketIO Events:
        - **connect**: Triggered when a client connects to the WebSocket.
        - **disconnect**: Triggered when a client disconnects from the WebSocket.
        - **message**: Client sends a message, server processes and responds with the reversed message.
        """
        return {"message": "This endpoint is for documentation purposes only"}, 200
