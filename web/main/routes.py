import re
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from web import db
from web.api.models import User, SocialLink, UserBio
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
    # Restrict available languages from users
    from web.data.language_loader import LANGUAGE_DATA

    username = session.get("user")
    user = User.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        display_name = request.form.get('display_name', '').strip()
        languages_raw = request.form.get('languages_data', '')
        units_raw = request.form.get('units_data', '')
        bio_raw = request.form.get('bio', '').strip()

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
        if not languages:
            flash('Please select at least one language.', 'danger')
            return redirect(url_for('main.edit_profile'))

        if not units:
            flash('Please add at least one study unit.', 'danger')
            return redirect(url_for('main.edit_profile'))
        
        # Validate languages against languages.json
        for language in languages:
            if language not in LANGUAGE_DATA:
                flash(f'Invalid language selected: {language}', 'danger')
                return redirect(url_for('main.edit_profile'))

        # Validate UWA unit format, e.g. CITS3403
        for unit in units:
            if not re.match(r'^[A-Z]{4}[0-9]{4}$', unit):
                flash(f'Invalid unit code: {unit}', 'danger')
                return redirect(url_for('main.edit_profile'))

        bio_entry = UserBio.query.filter_by(username=user.username).first()
        user.displayname = display_name
        user.languages = languages
        user.units = units

        if bio_entry:
            bio_entry.bio_text = bio_raw
        else:
            bio_entry = UserBio(username=user.username,bio_text=bio_raw)
            db.session.add(bio_entry)

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.edit_profile'))

    return render_template('main/edit_profile.html', user=user)

@main.route('/update_socials', methods=['POST'])
@require_login
def update_socials():
    user = User.query.get(session["user"])
    PLATFORMS = ["instagram", "linkedin", "discord"]

    # clear existing
    SocialLink.query.filter_by(user_id=user.username).delete()

    for p in PLATFORMS:
        raw = request.form.get(p, "").strip()
        if not raw:
            continue

        value = raw.strip()
        if p == "instagram":
            # @username
            if value.startswith("@"):
                value = value[1:]

            # username only
            if not value.startswith("http"):
                value = f"https://www.instagram.com/{value}"

            # HTTPS URL validation
            if not value.startswith("https://www.instagram.com/"):
                return jsonify({
                    "status": "error",
                    "message": "Instagram must be a valid Instagram profile link or username"
                }), 400

        elif p == "linkedin":
            # username only
            if not value.startswith("http"):
                value = f"https://www.linkedin.com/in/{value}"

            # HTTPS URL validation
            if not (value.startswith("https://www.linkedin.com/in/") or value.startswith("https://www.linkedin.com/company/")):
                return jsonify({
                    "status": "error",
                    "message": "LinkedIn must be a valid LinkedIn profile or company link"
                }), 400

        elif p == "discord":
            # Discord can be a username, not necessarily a URL
            if len(value) > 50:
                return jsonify({
                    "status": "error",
                    "message": "Discord username is too long"
                }), 400

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

@main.route('/search')
@require_login
def search():
    query = request.args.get('q', '').strip()
    current_username = session.get('user')
 
    if not query:
        return render_template('main/search.html', query='', results=[])
 
    query_lower = query.lower()
    all_users = User.query.filter(User.username != current_username).all()
 
    results = []
    for u in all_users:
        if (query_lower in (u.username or '').lower()
            or query_lower in (u.displayname or '').lower()
            or (u.languages and any(query_lower in (l or '').lower() for l in u.languages))
            or (u.units and any(query_lower in (un or '').lower() for un in u.units))):
            results.append(u)
 
    return render_template('main/search.html', query=query, results=results)