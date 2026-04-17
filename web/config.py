import os
from datetime import timedelta

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"    
    SECRET_KEY = os.getenv("SECRET_KEY") or "dev-secret-key"   
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or "sqlite:///app.db"  
    SESSION_COOKIE_HTTPONLY = os.getenv("SESSION_COOKIE_HTTPONLY", "True").lower() == "true"
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv("SESSION_PERMANENT_LIFETIME", 1800))
    ) 
    TESTING = os.getenv("TESTING", "false").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
