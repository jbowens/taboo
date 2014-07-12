import os
from flask import Flask

app = Flask(__name__, static_url_path='', static_folder='static')

app.config.from_pyfile('../config/default.cfg')

# Setup blueprints
from blueprints.main import main
app.register_blueprint(main)
