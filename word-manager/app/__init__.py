import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='', static_folder='static')

app.config.from_pyfile('../config/default.cfg')

db = SQLAlchemy(app)

# Setup blueprints
from blueprints.main import main
app.register_blueprint(main)

# Setup the models
from models.word import Word
from models.prohibited_word import ProhibitedWord
