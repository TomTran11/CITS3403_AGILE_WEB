from flask import render_template, request, redirect, url_for, session, flash
from web import db
from web.api.models import User
from . import main
from web.auth.utils import require_login

# Home page
@main.route('/')
@main.route('/landing_page')
def landing_page():
    return render_template('main/landing_page.html')

# Dashboard
@main.route('/dashboard')
@require_login
def dashboard():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()
    return render_template('main/dashboard.html', user=user)

# Error page
@main.app_errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@main.route('/check-session')
def check_session():
    from flask import session
    return {"user": session.get("user")}