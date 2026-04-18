from flask import render_template, request
from . import main
from web.auth.utils import require_login

# Home page
@main.route('/')
@main.route('/landing_page')
def landing_page():
    return render_template('main/landing_page.html')

# About page
@main.route('/about')
def about():
    return render_template('main/about.html')

# Dashboard
@main.route('/dashboard')
@require_login
def dashboard():
    return render_template('main/dashboard.html')  

# Error page
@main.app_errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@main.route('/check-session')
def check_session():
    from flask import session
    return {"user": session.get("user")}