from flask_mail import Message
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer

class EmailService:
    def __init__(self, mail):
        self.mail = mail

    # =========================
    # TOKEN LOGIC
    # =========================
    def _get_serializer(self):
        return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    def generate_token(self, user):
        s = self._get_serializer()
        return s.dumps({
            "email": user.email,
            "version": user.reset_token_version
        }, salt='password-reset')

    def verify_token(self, token, expiration=3600):
        from web.api.models import User

        s = self._get_serializer()
        try:
            data = s.loads(token, salt='password-reset', max_age=expiration)
        except Exception:
            return None

        user = User.query.filter_by(email=data.get("email")).first()

        if not user:
            return None

        #  SINGLE USE CHECK
        if user.reset_token_version != data.get("version"):
            return None

        return user

    # =========================
    # EMAIL SENDER
    # =========================
    def send_email(self, subject, recipients, body, html=None):
        try:
            msg = Message(subject=subject, recipients=recipients, body=body, html=html)
            self.mail.send(msg)
            print(" EMAIL SENT")
        except Exception as e:
            print(" EMAIL ERROR:", e)

    # =========================
    # RESET EMAIL
    # =========================
    def send_reset_email(self, user):
        token = self.generate_token(user)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        body = f"""
                Hi {user.displayname},

                Click the link below to reset your password:

                {reset_url}

                If you did not request this, ignore this email.

                Thanks,
                UniApp Team
                """

        html = f"""
                <h3>Hi {user.displayname},</h3>
                <p>Click below to reset your password:</p>

                <a href="{reset_url}" style="
                    display:inline-block;
                    padding:10px 20px;
                    background:#ff9f43;
                    color:white;
                    text-decoration:none;
                    border-radius:5px;
                ">
                    Reset Password
                </a>
                """

        self.send_email(
            subject="Password Reset Request",
            recipients=[user.email],
            body=body,
            html=html
        )