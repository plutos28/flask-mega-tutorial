from flask import Flask

flask_app = Flask(__name__)

# import routes here instead because it needs to import the app variable
from app import routes




