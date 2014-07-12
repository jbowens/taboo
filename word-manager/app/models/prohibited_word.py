from app import db

class ProhibitedWord(db.Model):
    """
    Represents a prohibited word.
    """
    __tablename__ = 'prohibited_words'
    pwid = db.Column(db.Integer, primary_key=True)
    wid = db.Column(db.Integer, db.ForeignKey('words.wid', ondelete='cascade'), nullable=False)
    word = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.Integer, nullable=False, default=0)
