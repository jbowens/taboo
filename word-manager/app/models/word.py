from app import db
from prohibited_word import ProhibitedWord

class Word(db.Model):
    """
    Represents a primary word.
    """
    __tablename__ = 'words'
    wid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True)
    skipped = db.Column(db.Integer, nullable=False, default=0)
    correct = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum('unverified', 'approved', 'rejected', name="word_status"), nullable=False, default='unverified')
    source = db.Column(db.String(255))

    def get_prohibited_words(self):
        return ProhibitedWord.query.filter(ProhibitedWord.wid==self.wid) \
                .order_by(ProhibitedWord.rank).all()
