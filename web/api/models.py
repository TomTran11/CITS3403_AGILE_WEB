from sqlalchemy import JSON

from web import db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(75), primary_key=True, nullable=False)
    displayname = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    languages = db.Column(JSON, nullable=False)
    units = db.Column(JSON, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    reset_token_version = db.Column(db.Integer, default=0)

class UserBio(db.Model):
    __tablename__ = "user_bios"

    bio_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False)
    bio_text = db.Column(db.Text, nullable=True)

    user = db.relationship(
        "User",
        backref=db.backref("bio_entry", uselist=False)
    )

class QuizResult(db.Model):
    __tablename__ = "quiz_results"

    result_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False)
    quiz_name = db.Column(db.String(100), nullable=False)
    question_index = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "username",
            "quiz_name",
            "question_index",
            name="unique_user_quiz_question"
        ),
    )


class UserKeyword(db.Model):
    __tablename__ = "user_keywords"

    keyword_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    source_quiz = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "username",
            "keyword",
            name="uq_user_keyword"
        ),
    )