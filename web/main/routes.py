from flask import render_template, request, session
from . import main
from web.auth.utils import require_login

@main.route('/')
@main.route('/landing_page')
def landing_page():
    return render_template('main/landing_page.html')

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/dashboard')
@require_login
def dashboard():
    return render_template('main/dashboard.html')

@main.route('/profile')
@require_login
def profile():
    return render_template('main/profile.html')

@main.route('/edit_profile')
@require_login
def edit_profile():
    return render_template('main/edit_profile.html')

@main.app_errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@main.route('/check-session')
def check_session():
    return {"user": session.get("user")}