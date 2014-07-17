from app.blueprints.api import api
from app.models.word import Word
from app.exceptions import InvalidUsage
from app import db
from flask import request, current_app, jsonify

@api.route('/reject', methods=['POST'])
def reject():
    wid = request.form.get('wid')
    if not wid:
        raise InvalidUsage('no wid in request')

    word = Word.query.filter(Word.wid == wid).first_or_404()
    word.status = 'rejected'
    db.session.add(word)
    db.session.commit()

    return jsonify(status='ok')
