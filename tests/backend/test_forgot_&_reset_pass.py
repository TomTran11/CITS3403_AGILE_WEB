"""
Password reset unit tests.

These tests check:
1. Forgot password rejects invalid email format
2. Forgot password accepts valid UWA student email format
3. Forgot password sends reset email when user exists
4. Reset password rejects invalid token on GET
5. Reset password rejects invalid token on POST

Notes:
- The forgot password endpoint should validate the email format and return appropriate responses.
- The reset password endpoint should validate the token and redirect to login if invalid.
- For the forgot password tests, we mock the email service to verify that it is called when a valid user email is provided.
"""
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User

# Helper function to create a test user
def create_test_user(username="resetuser", email="12345678@student.uwa.edu.au"):
    user = User(
        username=username,
        displayname="Reset User",
        password=generate_password_hash("oldpassword123"),
        languages=["English"],
        units=["CITS3403"],
        email=email
    )

    db.session.add(user)
    db.session.commit()

    return user

def test_forgot_password_invalid_email_rejected(client):
    response = client.post("/auth/forgot-password", data={
        "email": "test@student.uwa.edu.au"
    })

    assert response.status_code == 400 
    assert response.is_json
    assert response.get_json()["error"] == "Invalid email" 

def test_forgot_password_valid_email_format_accepted(client):
    response = client.post("/auth/forgot-password", data={
        "email": "12345678@student.uwa.edu.au"
    })

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()["message"] == "If the email exists, a reset link has been sent."

def test_forgot_password_existing_user_calls_email_service(client, monkeypatch):
    with client.application.app_context():
        create_test_user(username="resetuser", email="12345678@student.uwa.edu.au")

    email_called = {"called": False}

    def fake_send_reset_email(user):
        email_called["called"] = True
        assert user.email == "12345678@student.uwa.edu.au" 

    monkeypatch.setattr(
        client.application.email_service,
        "send_reset_email",
        fake_send_reset_email
    )

    response = client.post("/auth/forgot-password", data={
        "email": "12345678@student.uwa.edu.au"
    })

    assert response.status_code == 200 
    assert response.get_json()["message"] == "If the email exists, a reset link has been sent."
    assert email_called["called"] is True

def test_reset_password_invalid_token_get_redirects_to_login(client):
    response = client.get("/auth/reset-password/fake-token", follow_redirects=False)
    assert response.status_code in [302, 303]  
    assert "/auth/login" in response.headers["Location"] 

def test_reset_password_invalid_token_post_redirects_to_login(client):
    response = client.post("/auth/reset-password/fake-token", data={
        "password": "newpassword123",
        "confirm_password": "newpassword123"
    }, follow_redirects=False)

    assert response.status_code in [302, 303] 
    assert "/auth/login" in response.headers["Location"]