from app import blueprint
from app.main import create_app, socketio
import os

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return dict()


if __name__ == '__main__':
    print('Starting the socketio server')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
