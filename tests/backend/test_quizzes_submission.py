"""
This tests the responses for when we are submitting a quiz.
    1. Submitting a direct quiz saves and returns keywords
    2. Submitting a category quiz returns one keyword
    3. Retaking a quiz replaces old answers and keywords
"""

import json
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User


def create_test_user(app, username="submituser", email="333444@student.uwa.edu.au"):
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

#These set out the pre-defined answers for the following quizzes
VALID_FOOD_ANSWERS = {str(i): 5 for i in range(1, 11)}
VALID_SOCIAL_ANSWERS = {str(i): 3 for i in range(1, 11)}


def test_submit_direct_quiz_returns_200(client, app):
    create_test_user(app)
    login(client, "submituser")
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_submit_direct_quiz_returns_keywords(client, app):
    create_test_user(app)
    login(client, "submituser")
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    data = response.get_json()
    assert "generated_keywords" in data
    assert len(data["generated_keywords"]) == 10


def test_submit_category_quiz_returns_one_keyword(client, app):
    create_test_user(app)
    login(client, "submituser")
    response = client.post(
        "/quizzes/social_energy/submit",
        data=json.dumps({"answers": VALID_SOCIAL_ANSWERS}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert len(response.get_json()["generated_keywords"]) == 1


def test_retaking_quiz_replaces_old_answers(client, app):
    create_test_user(app)
    login(client, "submituser")

    #To tests the resubmission of retaking a quiz, we do 2 complete opposite snapshots, the first quiz answers 5 for every question to get a bunch of keywords
    client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )

    #The second submission then anwers 1 for every question to ensure this retake receives no keywords
    low_answers = {str(i): 1 for i in range(1, 11)}
    response = client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": low_answers}),
        content_type="application/json"
    )
    assert response.status_code == 200
    #We then compare and ensure they generated keyword returns nothing as the second submission is more recent
    assert response.get_json()["generated_keywords"] == []