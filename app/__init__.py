from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from app.config import Config
from flask_cors import CORS
app = Flask(__name__, template_folder='../templates')  # Ensure this is correct
app.config.from_object(Config)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
CORS(app)

from app import routes