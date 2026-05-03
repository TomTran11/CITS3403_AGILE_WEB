import os
from datetime import timedelta

def str_to_bool(value, default=False):
    if value is None:
        return default
    return str(value).lower() in ("true", "1", "yes")


class Config:
    DEBUG = str_to_bool(os.getenv("FLASK_DEBUG"), False)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    TESTING = str_to_bool(os.getenv("TESTING"), False)

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = str_to_bool(os.getenv("SESSION_COOKIE_HTTPONLY"), True)
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = str_to_bool(os.getenv("SESSION_COOKIE_SECURE"), False)

    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv("SESSION_PERMANENT_LIFETIME", 1800))
    )

    WTF_CSRF_ENABLED = str_to_bool(os.getenv("CSRF_ENABLED"), True)

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = str_to_bool(os.getenv("MAIL_USE_TLS"), True)
    MAIL_USE_SSL = str_to_bool(os.getenv("MAIL_USE_SSL"), False)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Uniapp Support", os.getenv("MAIL_USERNAME"))
    MAIL_SUPPRESS_SEND = str_to_bool(os.getenv("MAIL_SUPPRESS_SEND"), False)

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True