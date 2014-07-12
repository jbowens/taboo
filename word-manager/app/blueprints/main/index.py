from flask import render_template, request
from app.blueprints.main import main

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')
