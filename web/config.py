import os
from datetime import timedelta

def str_to_bool(value, default=False):
    return str(value).lower() in ("true", "1", "yes") if value is not None else default

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"    
    SECRET_KEY = os.getenv("SECRET_KEY") or "dev-secret-key"  
    TESTING = str_to_bool(os.getenv("TESTING"), False) 
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SESSION_COOKIE_HTTPONLY = os.getenv("SESSION_COOKIE_HTTPONLY", "True").lower() == "true"
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv("SESSION_PERMANENT_LIFETIME", 1800))
    ) 
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    WTF_CSRF_ENABLED = True


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
