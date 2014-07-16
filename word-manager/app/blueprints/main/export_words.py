from app.blueprints.main import main
from app.models.word import Word
from app import db
from flask import render_template, request, current_app

@main.route('/export', methods=['GET'])
def export_words():
    return render_template('export.html')
