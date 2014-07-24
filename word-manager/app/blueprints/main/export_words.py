from app.blueprints.main import main
from app.models.word import Word
from app import db
from flask import render_template, request, jsonify

@main.route('/export', methods=['GET'])
def export_words():
    return render_template('export.html')

@main.route('/export/download', methods=['GET'])
def download():

    words = Word.query.filter(Word.status=='approved').order_by(Word.wid).all()
    word_dicts = []
    for w in words:
        wdict = dict()
        wdict['wid'] = w.wid
        wdict['word'] = w.word
        wdict['prohibited'] = []
        prohibited = w.get_prohibited_words()
        for p in prohibited:
            wdict['prohibited'].append(p.word)
        word_dicts.append(wdict)

    data = {'words': word_dicts}
    resp = jsonify(**data)
    resp.headers['Content-Disposition'] = 'attachment; filename=words.json'
    return resp
