from flask import jsonify, render_template, request, redirect, url_for, session, flash
from web import db
from web.api.models import User, SocialLink
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

@main.route('/profile')
@require_login
def profile():
    return render_template('main/profile.html')

@main.route('/edit_profile')
@require_login
def edit_profile():
    return render_template('main/edit_profile.html')

@main.route('/update_socials', methods=['POST'])
@require_login
def update_socials():
    user = User.query.get(session["user"])
    PLATFORMS = ["instagram", "linkedin", "discord"]

    # clear existing
    SocialLink.query.filter_by(user_id=user.username).delete()

    for p in PLATFORMS:
        raw = request.form.get(p)

        if raw:
            value = raw.strip()

            if not value:
                return jsonify({
                    "status": "error",
                    "message": f"{p.capitalize()} cannot be empty"
                })

            if value.lower().startswith("javascript:"):
                return jsonify({
                    "status": "error",
                    "message": "Invalid link format"
                })

            if not value.startswith("http"):
                value = "https://" + value

            if not value.startswith("https://"):
                return jsonify({
                    "status": "error",
                    "message": f"{p.capitalize()} must use HTTPS"
                })

            db.session.add(SocialLink(
                user_id=user.username,
                platform=p,
                link=value
            ))

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Social links updated successfully!"
    })

@main.route('/account_settings')
@require_login
def account_settings():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()
    return render_template('main/account_settings.html', user=user)

@main.app_errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@main.route('/check-session')
def check_session():
    return {"user": session.get("user")}