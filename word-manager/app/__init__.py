import os
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from exceptions import InvalidUsage

app = Flask(__name__, static_url_path='', static_folder='static')

app.config.from_pyfile('../config/default.cfg')

db = SQLAlchemy(app)

# Setup blueprints
from blueprints.api import api
from blueprints.main import main
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(main)

# Setup the models
from models.word import Word
from models.prohibited_word import ProhibitedWord

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code if error.status_code else 400
  return response

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
