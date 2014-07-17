from app.blueprints.main import main
from app.models.word import Word
from app import db
from flask import render_template, request, current_app

@main.route('/', methods=['GET'])
def index():
    verified_breakdown = (db.session.query(db.func.count(Word.wid)).\
                          filter(Word.status=='unverified').first()[0],\
                          db.session.query(db.func.count(Word.wid)).\
                          filter(Word.status=='approved').first()[0])

    return render_template('index.html', \
            verified_unverified=verified_breakdown)
