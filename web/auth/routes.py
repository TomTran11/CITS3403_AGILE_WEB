from flask import current_app, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash,check_password_hash
from . import auth
from web.auth.utils import redirect_if_logged_in
from web import db
from web.api.models import User
import re

@auth.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():   
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for('main.dashboard'))

        flash("Invalid username or password.", "danger")
        return render_template('auth/login.html', title="Login")
    
    session.pop("user", None)
    return render_template('auth/login.html', title="Login")


# SIGNUP
@auth.route('/signup', methods=['GET', 'POST'])
@redirect_if_logged_in
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        display_name = request.form.get('display_name')
        study_units = request.form.get('units_data')
        spoken_languages = request.form.get('languages_data')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # Basic validation
        if not all([username, display_name, study_units, spoken_languages, password, confirm_password, email]):
            flash('All fields are required.', 'danger')
            return render_template('auth/signup.html', title="Sign Up")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email) | (User.displayname == display_name)
        ).first()
        if existing_user:
            flash('Username, email, or display name already exists.', 'danger')
            return render_template('auth/signup.html', title="Sign Up")

        study_units = [u.strip() for u in study_units.split(',') if u.strip()]
        unit_regex = re.compile(r'^[A-Z]{4}[0-9]{4}$')
        if len(study_units) == 0:
            flash('Please add at least one study unit.', 'danger')
            return render_template('auth/signup.html')
        
        if not all(unit_regex.match(u) for u in study_units):
            flash('Invalid unit format (e.g. CITS3001)', 'danger')
            return render_template('auth/signup.html')
        
        spoken_languages = [l.strip() for l in spoken_languages.split(',') if l.strip()]
        if len(spoken_languages) == 0:
            flash('Please select at least one language.', 'danger')
            return render_template('auth/signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/signup.html')
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@student\.uwa\.edu\.au$', email):
            flash('Email must be a valid @student.uwa.edu.au address.', 'danger')
            return render_template('auth/signup.html')
        
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            displayname=display_name,
            password=hashed_password,
            languages=spoken_languages,   
            units=study_units,            
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    session.pop("user", None)
    return render_template('auth/signup.html', title="Sign Up")

# LOGOUT
@auth.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login'))

@auth.route('/about')
def about():
    return render_template('auth/about.html')

# FORGOT PASSWORD
@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email', '').strip().lower()

    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@student\.uwa\.edu\.au$', email):
        return jsonify({"error": "Invalid email"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        current_app.email_service.send_reset_email(user)

    return jsonify({"message": "ok"})

# RESET PASSWORD
@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = current_app.email_service.verify_token(token)

    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(request.url)

        if not new_password or len(new_password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(request.url)

        user.password = generate_password_hash(new_password)

        user.reset_token_version += 1
        db.session.commit()

        flash('Password updated successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')