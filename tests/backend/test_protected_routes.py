"""
Protected route unit tests.

These tests check that:
1. Logged-out users are redirected to the login page
2. Logged-in users can access protected pages
"""
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User

# Helper function to create a test user
def create_test_user(username="testuser", email="123456@student.uwa.edu.au"):
    user = User(
        username=username,
        displayname="Test User",
        password=generate_password_hash("password123"),
        languages=["English"],
        units=["CITS3403"],
        email=email
    )

    db.session.add(user)
    db.session.commit()
    return user

# Helper function to log in a test user by setting the session
def login_test_user(client, username="testuser"):
    with client.session_transaction() as session:
        session["user"] = username

def test_dashboard_redirects_when_logged_out(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code in [302, 303]
    assert "/auth/login" in response.headers["Location"]

def test_dashboard_loads_when_logged_in(client):
    with client.application.app_context():
        create_test_user(username="dashboarduser", email="111111@student.uwa.edu.au")

    login_test_user(client, username="dashboarduser")
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 200
    assert response.request.path == "/dashboard"

def test_profile_redirects_when_logged_out(client):
    response = client.get("/profile", follow_redirects=False)
    assert response.status_code in [302, 303]
    assert "/auth/login" in response.headers["Location"]

def test_profile_loads_when_logged_in(client):
    with client.application.app_context():
        create_test_user(username="profileuser", email="222222@student.uwa.edu.au")

    login_test_user(client, username="profileuser")
    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 200
    assert response.request.path == "/profile"

def test_edit_profile_redirects_when_logged_out(client):
    response = client.get("/edit_profile", follow_redirects=False)
    assert response.status_code in [302, 303]
    assert "/auth/login" in response.headers["Location"]

def test_edit_profile_loads_when_logged_in(client):
    with client.application.app_context():
        create_test_user(username="edituser", email="333333@student.uwa.edu.au")

    login_test_user(client, username="edituser")
    response = client.get("/edit_profile", follow_redirects=False)
    assert response.status_code == 200
    assert response.request.path == "/edit_profile"

def test_account_settings_redirects_when_logged_out(client):
    response = client.get("/account_settings", follow_redirects=False)
    assert response.status_code in [302, 303]
    assert "/auth/login" in response.headers["Location"]

def test_account_settings_loads_when_logged_in(client):
    with client.application.app_context():
        create_test_user(username="accountuser", email="444444@student.uwa.edu.au")

    login_test_user(client, username="accountuser")
    response = client.get("/account_settings", follow_redirects=False)
    assert response.status_code == 200
    assert response.request.path == "/account_settings"