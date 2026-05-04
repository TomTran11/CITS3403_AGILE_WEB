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

    social_links = db.relationship(
        'SocialLink',
        backref='user',
        cascade="all, delete-orphan",
        lazy=True
    )

class SocialLink(db.Model):
    __tablename__ = "social_links"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.String(75),
        db.ForeignKey('users.username'),
        nullable=False
    )

    platform = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    # Ensure a user can only have one link per platform
    __table_args__ = (
        db.UniqueConstraint('user_id', 'platform', name='unique_user_platform'),
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