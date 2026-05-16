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
def create_app(config_name):
    app = Flask(__name__)
    if config_name =="testing":
        app.config.from_object(TestingConfig)
        print("Using Testing config (explicit)")
    elif config_name=="production":
        app.config.from_object(DevelopmentConfig)
        print("Using Production config (explicit)")
    else:
        app.config.from_object(ProductionConfig)
        print("Using Development config (explicit)")


    mail.init_app(app)
    db.init_app(app)
    csrf.init_app(app)

    app.email_service = EmailService(mail)

    from web.main import main
    from web.auth import auth
    from web.api import api
    from web.quizzes import quizzes
    from web.matching import matching

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(quizzes, url_prefix="/quizzes")
    app.register_blueprint(matching)

    from web.api.models import User, QuizResult, UserKeyword, Notification

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_notifications():
        from web.api.models import Notification
        username = session.get("user")
        if not username:
            return {"recent_notifications": [], "unread_notification_count": 0}

        recent_notifications = Notification.query.filter_by(user_id=username).order_by(Notification.created_at.desc()).limit(10).all()
        unread_count = Notification.query.filter_by(user_id=username, is_read=False).count()
        return {"recent_notifications": recent_notifications, "unread_notification_count": unread_count}
    
    return app

# create module-level app for convenience
app = create_app(os.getenv("FlASK_CONFIG","development").lower())