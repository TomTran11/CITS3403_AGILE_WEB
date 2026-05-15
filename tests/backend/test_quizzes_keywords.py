"""
This tests the quizzes keywords endpoints to ensure keywords when called upon return the correct data
    1. Keywords endpoint requires login
    2. Keywords returns 404 for invalid quiz
    3. Keywords returns empty before submission
    4. Keywords returns correct keywords after submission
    5. Keywords only returns keywords for specified quiz
"""

import json
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User


def create_test_user(app, username="keywordsuser", email="777888@student.uwa.edu.au"):
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


VALID_FOOD_ANSWERS = {str(i): 5 for i in range(1, 11)}
VALID_SOCIAL_ANSWERS = {str(i): 3 for i in range(1, 11)}


def test_keywords_requires_login(client):
    response = client.get(
        "/quizzes/food_preferences/keywords",
        follow_redirects=False
    )
    assert response.status_code in [302, 303]


def test_keywords_returns_404_for_invalid_quiz(client, app):
    create_test_user(app)
    login(client, "keywordsuser")
    response = client.get("/quizzes/made_up_quiz/keywords")
    assert response.status_code == 404


def test_keywords_empty_before_submission(client, app):
    create_test_user(app)
    login(client, "keywordsuser")
    response = client.get("/quizzes/food_preferences/keywords")
    assert response.status_code == 200
    assert response.get_json()["keywords"] == []


def test_keywords_returns_correct_keywords_after_submission(client, app):
    create_test_user(app)
    login(client, "keywordsuser")
    client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    response = client.get("/quizzes/food_preferences/keywords")
    assert response.status_code == 200
    assert len(response.get_json()["keywords"]) == 10


def test_keywords_only_returns_keywords_for_specified_quiz(client, app):
    create_test_user(app)
    login(client, "keywordsuser")
    client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    client.post(
        "/quizzes/social_energy/submit",
        data=json.dumps({"answers": VALID_SOCIAL_ANSWERS}),
        content_type="application/json"
    )
    food_keywords = client.get("/quizzes/food_preferences/keywords").get_json()["keywords"]
    social_keywords = client.get("/quizzes/social_energy/keywords").get_json()["keywords"]
    assert len(food_keywords) == 10
    assert len(social_keywords) == 1
    for kw in social_keywords:
        assert kw not in food_keywords