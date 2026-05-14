from flask import Flask,session
from dotenv import load_dotenv
load_dotenv()
from web.config import ProductionConfig, DevelopmentConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail
from web.services.mail_service import EmailService
import os


db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
app = Flask(__name__)
config_name=os.getenv("FlASK_CONFIG","development").lower()

if config_name=="testing":
    app.config.from_object(TestingConfig)
    print("Using Testing config")
elif config_name=="production":
    app.config.from_object(DevelopmentConfig)
    print("Using Production config")
else:
    app.config.from_object(ProductionConfig)
    print("Using Development config")

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

from web.matching import matching
app.register_blueprint(matching)


with app.app_context():
    db.create_all()

@app.context_processor
def inject_notifications():
    from web.api.models import Notification

    username = session.get("user")

    if not username:
        return {"recent_notifications": [],"unread_notification_count": 0}

    recent_notifications = Notification.query.filter_by(user_id=username).order_by(Notification.created_at.desc()).limit(10).all()

    return {"recent_notifications": recent_notifications}