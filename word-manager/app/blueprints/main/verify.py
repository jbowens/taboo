from app.blueprints.main import main
from app.models.word import Word
from app import db
from flask import render_template, request, current_app
from sqlalchemy import func

@main.route('/verify-words', methods=['GET'])
def verify_words():
  word = Word.query.filter(Word.status=='unverified').order_by(func.random()).first()
  if word:
    return render_template('verify_word.html', \
            word=word, \
            prohibited_words = word.get_prohibited_words())
  return render_template('verify_word.html', \
          word=word)
