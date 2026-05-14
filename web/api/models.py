from sqlalchemy import JSON
from datetime import datetime
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
    social_links = db.relationship('SocialLink',backref='user',cascade="all, delete-orphan",lazy=True)
    likes_given = db.relationship("ProfileLike",foreign_keys="ProfileLike.liker_username",backref="liker",lazy="dynamic",cascade="all, delete-orphan")
    likes_received = db.relationship("ProfileLike",foreign_keys="ProfileLike.liked_username",backref="liked",lazy="dynamic",cascade="all, delete-orphan")
    
class UserBio(db.Model):
    __tablename__ = "user_bios"

    bio_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False, unique=True)
    bio_text = db.Column(db.Text, nullable=True)

    user = db.relationship("User",backref=db.backref("bio_entry", uselist=False))

class SocialLink(db.Model):
    __tablename__ = "social_links"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(75),db.ForeignKey('users.username'),nullable=False)

    platform = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    # Ensure a user can only have one link per platform
    __table_args__ = (
        db.UniqueConstraint('user_id', 'platform', name='unique_user_platform'),
    )

class ProfileLike(db.Model):
    __tablename__ = "profile_likes"

    id = db.Column(db.Integer, primary_key=True)
    liker_username = db.Column(db.String(75),db.ForeignKey("users.username"),nullable=False,index=True)
    liked_username = db.Column(db.String(75),db.ForeignKey("users.username"),nullable=False,index=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    __table_args__ = (
        db.UniqueConstraint("liker_username","liked_username",name="unique_profile_like"),
        db.CheckConstraint("liker_username != liked_username",name="no_self_like"),
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