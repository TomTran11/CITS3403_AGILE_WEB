from flask import Flask
from dotenv import load_dotenv
from web.config import ProductionConfig, DevelopmentConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail
from web.services.mail_service import EmailService
import os

load_dotenv()
db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
app = Flask(__name__)
testing = os.getenv("TESTING", "false").lower() == "true"
debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

if testing:
    app.config.from_object(TestingConfig)
elif debug:
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

mail.init_app(app)
db.init_app(app)
csrf.init_app(app)   

# Services registration
app.email_service = EmailService(mail)

# Importing and registering blueprints
from web.main import main
from web.auth import auth
from web.api import api
from web.quizzes import quizzes
app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(quizzes, url_prefix="/quizzes")

from web.api.models import User


with app.app_context():
    db.create_all()