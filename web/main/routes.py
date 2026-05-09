import re
from flask import render_template, request, redirect, url_for, session, flash
from web import db
from web.api.models import User
from . import main
from web.auth.utils import require_login

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

@main.route('/about')
def about():
    return render_template('auth/about.html')

# Profile (view)
@main.route('/profile')
@require_login
def profile():
    username = session.get("user")
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/profile.html', user=user)

# Edit profile (GET + POST)
@main.route('/edit_profile', methods=['GET', 'POST'])
@require_login
def edit_profile():
    username = session.get("user")
    user = User.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        display_name = request.form.get('display_name', '').strip()
        languages_raw = request.form.get('languages_data', '')
        units_raw = request.form.get('units_data', '')

        if not display_name:
            flash('Display name is required.', 'danger')
            return redirect(url_for('main.edit_profile'))

        if display_name != user.displayname:
            existing = User.query.filter(
                User.displayname == display_name,
                User.username != user.username
            ).first()
            if existing:
                flash('Display name already taken.', 'danger')
                return redirect(url_for('main.edit_profile'))

        languages = [l.strip() for l in languages_raw.split(',') if l.strip()]
        units = [u.strip().upper() for u in units_raw.split(',') if u.strip()]

        user.displayname = display_name
        user.languages = languages
        user.units = units
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('main/edit_profile.html', user=user)

@main.route('/account_settings')
@require_login
def account_settings():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()
    return render_template('main/account_settings.html', user=user)

@main.route('/notifications')
@require_login
def notifications():
    return render_template('main/notifications.html')

@main.app_errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@main.route('/check-session')
def check_session():
    return {"user": session.get("user")}