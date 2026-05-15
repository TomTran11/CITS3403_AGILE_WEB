"""
This tests the completed quiz section of the quizzes page
    2. Completed quiz section returns empty list before submission
    3. Completed quiz section returns the quiz after submission
    4. Completed quiz section returns multiple quizzes after multiple submissions
    5. Completed quiz section has no duplicates after retake
"""

import json
from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User


def create_test_user(app, username="completeduser", email="999000@student.uwa.edu.au"):
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

#This tests if the completed section is empty as a new user wont have done any quizzes
def test_completed_empty_before_submission(client, app):
    create_test_user(app)
    login(client, "completeduser")
    response = client.get("/quizzes/completed")
    assert response.status_code == 200
    assert response.get_json()["completed_quizzes"] == []

#This then tests that the completed section has the correct quiz after it is submitted and finished
def test_completed_returns_quiz_after_submission(client, app):
    create_test_user(app)
    login(client, "completeduser")
    client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    response = client.get("/quizzes/completed")
    assert "food_preferences" in response.get_json()["completed_quizzes"]

#This tests when the user has completed multiple quizzes and that they are also all represented in the completed section
def test_completed_returns_multiple_quizzes(client, app):
    create_test_user(app)
    login(client, "completeduser")
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
    completed = client.get("/quizzes/completed").get_json()["completed_quizzes"]
    assert "food_preferences" in completed
    assert "social_energy" in completed

#We also have to critically test that there are no duplicate cards in the quizzes page, and that it was correctly moved from one section to the other
def test_completed_no_duplicates_after_retake(client, app):
    create_test_user(app)
    login(client, "completeduser")
    client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    client.post(
        "/quizzes/food_preferences/submit",
        data=json.dumps({"answers": VALID_FOOD_ANSWERS}),
        content_type="application/json"
    )
    completed = client.get("/quizzes/completed").get_json()["completed_quizzes"]
    assert completed.count("food_preferences") == 1