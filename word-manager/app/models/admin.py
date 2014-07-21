from app import db

class Admin(db.Model):
    """
    Represents an administrator.
    """
    __tablename__ = 'admins'
    aid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    passwordhash = db.Column(db.String(256))
