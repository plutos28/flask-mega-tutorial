from flask import Flask
from config import Config

flask_app = Flask(__name__)
flask_app.config.from_object(Config)

# import routes here instead because it needs to import the app variable
from app import routes




