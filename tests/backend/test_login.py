"""
Login unit tests.

These tests check:
1. Login page loads
2. Wrong username is rejected
3. Wrong password is rejected
4. Empty username and password are rejected
5. Correct login sets the session

Notes:
- Invalide login attempts should return the login page with an error message.
- A successful login should redirect to the dashboard and set the session user.
"""
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User

def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200  
    assert response.request.path == "/auth/login"  

def test_login_wrong_username_rejected(client):
    response = client.post("/auth/login", data={
        "username": "fakeuser",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200  
    assert response.request.path == "/auth/login"  

def test_login_wrong_password_rejected(client):
    user = User(
        username="testuser",
        displayname="Test User",
        email="111111@student.uwa.edu.au",
        password=generate_password_hash("correctpassword"),
        languages=["English"],
        units=["CITS3403"]
    )

    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert response.status_code == 200  
    assert response.request.path == "/auth/login"  

def test_login_empty_username_and_password_rejected(client):
    response = client.post("/auth/login", data={
        "username": "",
        "password": ""
    }, follow_redirects=True)

    assert response.status_code == 200  
    assert response.request.path == "/auth/login"  

def test_login_correct_details_sets_session(client):
    user = User(
        username="testuser2",
        displayname="Test User 2",
        email="222222@student.uwa.edu.au",
        password=generate_password_hash("correctpassword"),
        languages=["English"],
        units=["CITS3403"]
    )

    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", data={
        "username": "testuser2",
        "password": "correctpassword"
    }, follow_redirects=True)

    assert response.status_code == 200  
    assert response.request.path == "/dashboard"  

    with client.session_transaction() as session:
        assert session["user"] == "testuser2"  