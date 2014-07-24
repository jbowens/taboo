from app.blueprints.api import api
from app.models.word import Word
from app.exceptions import InvalidUsage
from app import db
from flask import request, jsonify, current_app

@api.route('/search', methods=['POST'])
def search():
    q = request.form.get('q')
    if not q:
        raise InvalidUsage('no search query in request')

    words = Word.query.filter(Word.word.like('%' + q + '%')).all()

    resp = dict()
    resp['status'] = 'ok'
    resp['results'] = []

    for w in words:
        wdict = dict()
        wdict['wid'] = w.wid
        wdict['word'] = w.word
        wdict['status'] = w.status
        resp['results'].append(wdict)

    return jsonify(**resp)
