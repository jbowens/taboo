from app.blueprints.api import api
from app.models.prohibited_word import ProhibitedWord
from app.exceptions import InvalidUsage
from app import db
from flask import request, jsonify

@api.route('/add-prohibited', methods=['POST'])
def add_prohibited():
  wid = request.form.get('wid')
  word = request.form.get('word')
  if not wid or not word:
    raise InvalidUsage('not enough information in request')

  max_rank = db.session.query(db.func.max(ProhibitedWord.rank)).\
      filter(ProhibitedWord.wid==wid).first()[0]

  pw = ProhibitedWord()
  pw.wid = wid
  pw.word = word
  pw.rank = max_rank + 1
  db.session.add(pw)
  db.session.commit()

  return jsonify(status='ok', pwid=pw.pwid, rank=pw.rank)
