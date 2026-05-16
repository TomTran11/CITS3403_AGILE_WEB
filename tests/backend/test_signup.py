"""
Signup unit tests.

These tests check:
1. Signup page loads
2. Missing required fields are rejected
3. Invalid unit format is rejected
4. Password and confirm password mismatch is rejected
5. Invalid/non-UWA email is rejected
6. Valid signup creates a new user and redirects to login
7. Duplicate username/display name/email is rejected

Notes:
 - Invalide cases, the expected destination is always "/auth/signup" with a 200 status code
 - Valid signup should redirect to "/auth/login" with a 200 status code
"""
from werkzeug.security import check_password_hash
from web import db
from web.api.models import User

def test_signup_page_loads(client):
    response = client.get("/auth/signup")
    assert response.status_code == 200
    assert response.request.path == "/auth/signup"

def test_signup_missing_fields_rejected(client):
    response = client.post("/auth/signup", data={
        "username": "",
        "display_name": "",
        "units_data": "",
        "languages_data": "",
        "password": "",
        "confirm_password": "",
        "email": ""
    })

    assert response.status_code == 200
    assert response.request.path == "/auth/signup"

def test_signup_invalid_unit_format_rejected(client):
    response = client.post("/auth/signup", data={
        "username": "testuser",
        "display_name": "Test User",
        "units_data": "INVALID123",
        "languages_data": "English",
        "password": "password123",
        "confirm_password": "password123",
        "email": "123456@student.uwa.edu.au"
    })

    assert response.status_code == 200
    assert response.request.path == "/auth/signup"

def test_signup_password_mismatch_rejected(client):
    response = client.post("/auth/signup", data={
        "username": "testuser",
        "display_name": "Test User",
        "units_data": "CITS3403",
        "languages_data": "English",
        "password": "password123",
        "confirm_password": "differentpassword",
        "email": "123456@student.uwa.edu.au"
    })

    assert response.status_code == 200
    assert response.request.path == "/auth/signup"

def test_signup_invalid_email_rejected(client):
    response = client.post("/auth/signup", data={
        "username": "testuser",
        "display_name": "Test User",
        "units_data": "CITS3403",
        "languages_data": "English",
        "password": "password123",
        "confirm_password": "password123",
        "email": "test@student.uwa.edu.au"
    })

    assert response.status_code == 200
    assert response.request.path == "/auth/signup"

def test_signup_valid_user_created(client):
    response = client.post("/auth/signup", data={
        "username": "newuser",
        "display_name": "New User",
        "units_data": "CITS3403",
        "languages_data": "English",
        "password": "password123",
        "confirm_password": "password123",
        "email": "123456@student.uwa.edu.au"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/auth/login"

    with client.application.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert user.displayname == "New User"
        assert user.email == "123456@student.uwa.edu.au"
        assert user.languages == ["English"]
        assert user.units == ["CITS3403"]
        assert check_password_hash(user.password, "password123")

def test_signup_duplicate_user_rejected(client):
    existing_user = User(
        username="existinguser",
        displayname="Existing User",
        password="hashed-password-placeholder",
        languages=["English"],
        units=["CITS3403"],
        email="654321@student.uwa.edu.au"
    )

    with client.application.app_context():
        db.session.add(existing_user)
        db.session.commit()

    response = client.post("/auth/signup", data={
        "username": "existinguser",
        "display_name": "Another User",
        "units_data": "CITS3403",
        "languages_data": "English",
        "password": "password123",
        "confirm_password": "password123",
        "email": "123456@student.uwa.edu.au"
    })

    assert response.status_code == 200
    assert response.request.path == "/auth/signup"