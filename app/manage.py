from app import blueprint
from app.main import create_app
import os

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return dict()