from app.blueprints.api import api
from app.models.prohibited_word import ProhibitedWord
from app.exceptions import InvalidUsage
from app import db
from flask import request, current_app, jsonify

@api.route('/remove-prohibited', methods=['POST'])
def remove_prohibited():
  pwid = request.form.get('pwid')
  if not pwid:
    raise InvalidUsage('no pwid in request')

  pw = ProhibitedWord.query.filter(ProhibitedWord.pwid == pwid).first_or_404()
  db.session.delete(pw)
  db.session.commit()

  return jsonify(status='ok')
