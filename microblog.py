from app import flask_app
from app import db
from app.models import User, Post

@flask_app.shell_context_processor
def make_shell_context():
    # pre-import symbols to flask shell so that you don't have
    # to import each time
    return {'db': db, 'User': User, 'Post': Post}
