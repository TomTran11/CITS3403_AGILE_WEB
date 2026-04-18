from web import db

class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(75), primary_key=True, nullable=False)
    displayname = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    languages = db.Column(db.String(100), nullable=False)
    studyunits = db.Column(db.String(45), nullable=False)