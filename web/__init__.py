from flask import Flask
from dotenv import load_dotenv
from web.config import ProductionConfig, DevelopmentConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()
db = SQLAlchemy()
app = Flask(__name__)
env = os.getenv("FLASK_ENV", "development")
testing = os.getenv("TESTING", "false").lower() == "true"

if testing:
    app.config.from_object(TestingConfig)
elif env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db.init_app(app)


# Importing and registering blueprints
from web.main import main
from web.auth import auth
from web.api import api
app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')

from web.api.models import User

with app.app_context():
    db.create_all()