import re
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from web import db
from web.api.models import User, SocialLink, UserBio, Notification
from . import main
from web.matching.service import find_matches_for_user
from web.auth.utils import require_login
from web.main.services import like_user, unlike_user,get_liked_usernames, has_mutual_like ,update_user_socials, delete_user_social
from web.matching.service import find_matches_for_user, get_answers_for_user


@main.route('/')
@main.route('/landing_page')
def landing_page():
    return render_template('main/landing_page.html', title="Landing Page")

# Dashboard
@main.route('/dashboard')
@require_login
def dashboard():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()
    threshold = request.args.get("threshold", default=10, type=int)

    #This calls the matching logic in service.py
    matches = find_matches_for_user(username, threshold)
    for i in range(len(matches)):
        item = matches[i]
        matchedUser = User.query.filter_by(username=item["username"]).first()
        matches[i] = matchedUser

    # Get everyone this current user has already liked
    liked_usernames = get_liked_usernames(username)
    return render_template('main/dashboard.html', user=user, matches=matches, liked_usernames=liked_usernames)





# View a user's profile
@main.route('/view_user/<username>' )
@require_login
def view_user(username):
    viewed_user = User.query.filter_by(username=username).first_or_404()
    username = session.get("user")
    user = User.query.filter_by(username=username).first_or_404()
    
    return render_template('main/profile.html', user=user, viewed_user = viewed_user)

# Profile (view)
@main.route('/profile')
@require_login
def profile():
    username = session.get("user")
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/profile.html', user=user, viewed_user = user)

@main.route("/profile/<displayname>", methods=["GET"])
@require_login
def view_profile(displayname):
    current_username = session.get("user")
    current_user = User.query.filter_by(username=current_username).first_or_404()
    other_user = User.query.filter_by(displayname=displayname).first_or_404()
    
    # View owned profile
    if other_user.username == current_username:
        return redirect(url_for("main.profile"))

    # View others profile
    if not has_mutual_like(current_user.username, other_user.username):
        flash("You can only view social contacts for users you have matched with.", "warning")
        return redirect(url_for("main.dashboard"))

    return render_template('main/profile.html', user=current_user, viewed_user=other_user)

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
            bio_entry = UserBio(username=user.username, bio_text=bio_raw)
            db.session.add(bio_entry)

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.edit_profile'))

    return render_template('main/edit_profile.html', user=user)

@main.route('/update_socials', methods=['POST'])
@require_login
def update_socials():
    user = User.query.get(session["user"])

    try:
        update_user_socials(user, request.form)

        return jsonify({
            "status": "success",
            "message": "Social links updated successfully!"
        })

    except ValueError as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    except Exception:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Something went wrong while updating social links"
        }), 500


@main.route("/delete_social/<platform>", methods=["POST"])
@require_login
def delete_social(platform):
    user = User.query.get(session["user"])

    try:
        deleted = delete_user_social(user, platform)

        if not deleted:
            return jsonify({
                "status": "error",
                "message": "Social link not found"
            }), 404

        return jsonify({
            "status": "success",
            "message": f"{platform.title()} removed successfully"
        })

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    except Exception:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Something went wrong while deleting social link"
        }), 500
    
@main.route("/account_settings", methods=["GET", "POST"])
@require_login
def account_settings():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()

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
    current_username = session.get("user")
    user = User.query.filter_by(username=current_username).first_or_404()
    notifications = Notification.query.filter_by(user_id=current_username).order_by(Notification.created_at.desc()).all()
    related_ids = {n.related_user_id for n in notifications if n.related_user_id}
    related_map = {}
    if related_ids:
        users = User.query.filter(User.username.in_(related_ids)).all()
        related_map = {u.username: u.displayname for u in users}

    for n in notifications:
        n.related_displayname = related_map.get(n.related_user_id) if n.related_user_id else None

    return render_template("main/notifications.html", user=user, notifications=notifications)

# Matching page (full list of matches)
@main.route('/matches')
@require_login
def matching():
    username = session.get("user")
    user = User.query.filter_by(username=username).first()
    threshold = request.args.get("threshold", default=10, type=int)
 
    # Determine if the user has taken any quizzes
    # (needed to distinguish "no quizzes done" from "no matches found")
    has_quizzes = bool(get_answers_for_user(username))
 
    # Get matches — will be [] if user hasn't taken quizzes OR no users meet threshold
    matches = find_matches_for_user(username, threshold)
    # Enrich each match dict with the full User object (same pattern as dashboard)
    for i in range(len(matches)):
        item = matches[i]
        matchedUser = User.query.filter_by(username=item["username"]).first()
        matches[i] = matchedUser
 
    liked_usernames = get_liked_usernames(username)
 
    return render_template(
        'main/matching.html',
        user=user,
        matches=matches,
        liked_usernames=liked_usernames,
        has_quizzes=has_quizzes
    )
 

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

@main.route("/profile/<username>/like", methods=["POST"])
@require_login
def like_profile(username):
    current_username = session.get("user")
    result = like_user(liker_username=current_username,liked_username=username)
    status_code = result.pop("status_code")
    if result.get("match"):
        flash(f"It's a match with {username}!", "success")
    return jsonify(result), status_code

@main.route("/profile/<username>/unlike", methods=["POST"])
@require_login
def unlike_profile(username):
    current_username = session.get("user")
    result = unlike_user(liker_username=current_username,liked_username=username)
    status_code = result.pop("status_code")
    return jsonify(result), status_code
