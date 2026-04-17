from flask import render_template, request, redirect, url_for, session
from . import auth
from web.auth.utils import redirect_if_logged_in

# LOGIN
@auth.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():   
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(username, password)
        session["user"] = username

        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html')


# SIGNUP
@auth.route('/signup', methods=['GET', 'POST'])
@redirect_if_logged_in
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print("New user:", username)

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')

# LOGOUT
@auth.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login'))