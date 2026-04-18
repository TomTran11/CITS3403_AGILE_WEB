from functools import wraps
from flask import session, redirect, url_for

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user"):
            return redirect(url_for('main.dashboard'))  
        return f(*args, **kwargs)
    return decorated_function