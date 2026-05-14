"""
This tests the quizzes validation when it comes to submitted a quiz.
    1. Submitting a quiz requires login
    2. Submitting with missing answers is rejected
    3. Submitting with score too low is rejected
    4. Submitting with score too high is rejected
    5. Submitting with no data is rejected
"""

import json
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User


def create_test_user(app, username="validuser", email="555666@student.uwa.edu.au"):
    with app.app_context():
        user = User(
            username=username,
            displayname=username,
            password=generate_password_hash("P@ssword123"),
            languages=["English"],
            units=["CITS3403"],
            email=email,
            reset_token_version=0
        )
        db.session.add(user)
        db.session.commit()

#This simulates a logged in session
def login(client, username):
    with client.session_transaction() as session:
        session["user"] = username

#And this checks that a redirect is confirmed when a non logged in user attempts a quiz submission
def test_submit_quiz_requires_login(client):
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": {str(i): 3 for i in range(1, 11)}}),
        content_type="application/json",
        follow_redirects=False
    )
    assert response.status_code in [302, 303]


def test_submit_missing_answer_rejected(client, app):
    create_test_user(app)
    login(client, "validuser")
    incomplete = {str(i): 3 for i in range(1, 10)}
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": incomplete}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_submit_score_too_low_rejected(client, app):
    create_test_user(app)
    login(client, "validuser")
    bad_answers = {str(i): 0 for i in range(1, 11)}
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": bad_answers}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_submit_score_too_high_rejected(client, app):
    create_test_user(app)
    login(client, "validuser")
    bad_answers = {str(i): 6 for i in range(1, 11)}
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": bad_answers}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_submit_no_data_rejected(client, app):
    create_test_user(app)
    login(client, "validuser")
    response = client.post(
        "/quizzes/food_preferences/submit",
        content_type="application/json"
    )
    assert response.status_code == 400