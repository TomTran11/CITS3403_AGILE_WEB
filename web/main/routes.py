from flask import jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
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

@main.route("/account_settings", methods=["GET", "POST"])
@require_login
def account_settings():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_new_password", "")
        current_password = request.form.get("current_password", "")

        # Check current password
        if not check_password_hash(user.password, current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("main.account_settings"))
        
        # No changes entered
        if not email and not new_password and not confirm_password:
            flash("No changes were made.", "warning")
            return redirect(url_for("main.account_settings"))

        # Current password required before any update
        if not current_password:
            flash("Please enter your current password.", "danger")
            return redirect(url_for("main.account_settings"))

        # Update email only if user entered a new email
        if email:
            if not email.endswith("@student.uwa.edu.au"):
                flash("Email must be a valid UWA student email.", "danger")
                return redirect(url_for("main.account_settings"))

            existing_email = User.query.filter(
                User.email == email,
                User.username != user.username
            ).first()

            if existing_email:
                flash("This email is already used by another account.", "danger")
                return redirect(url_for("main.account_settings"))

            user.email = email

        # Update password only if user entered a new password
        if new_password or confirm_password:
            if new_password != confirm_password:
                flash("New password and confirm password do not match.", "danger")
                return redirect(url_for("main.account_settings"))

            if len(new_password) < 6:
                flash("Password must be at least 6 characters long.", "danger")
                return redirect(url_for("main.account_settings"))

            user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Account settings updated successfully.", "success")
        return redirect(url_for("main.account_settings"))

    return render_template("main/account_settings.html", user=user)

@main.app_errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@main.route('/check-session')
def check_session():
    return {"user": session.get("user")}

# Notifications page
@main.route('/notifications')
@require_login
def notifications():
    return render_template('main/notifications.html')