"""
This tests the quizzes routes:
    1. Getting a valid quiz returns 200 and correct data
    2. Getting a valid quiz returns 10 questions
    3. Getting an invalid quiz returns 404
"""

from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User


def create_test_user(app, username="routeuser", email="111222@student.uwa.edu.au"):
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


def login(client, username):
    with client.session_transaction() as session:
        session["user"] = username


def test_get_valid_quiz_returns_200(client):
    response = client.get("/quizzes/food_preferences")
    assert response.status_code == 200


def test_get_valid_quiz_returns_correct_data(client):
    response = client.get("/quizzes/food_preferences")
    data = response.get_json()
    assert "questions" in data


def test_get_valid_quiz_returns_10_questions(client):
    response = client.get("/quizzes/food_preferences")
    data = response.get_json()
    assert len(data["questions"]) == 10


def test_get_invalid_quiz_returns_404(client):
    response = client.get("/quizzes/made_up_quiz")
    assert response.status_code == 404


def test_get_invalid_quiz_returns_error_message(client):
    response = client.get("/quizzes/made_up_quiz")
    assert "error" in response.get_json()