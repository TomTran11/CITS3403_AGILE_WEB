"""
This tests the quizzes matching routes
    1. Matching endpoint requires login
    2. User with no quiz answers returns empty matches
    3. Two users with identical answers will get a 100% match
    4. Two users with the opposite answers will get a 0% match
    5. Users with no overlapping quizzes are not matched at all
    6. Users below default threshold are not returned
    7. Matches are sorted highest to lowest
    8. Custom threshold via query parameter works
    9. Match percentage is calculated correctly
    10. Shared quizzes are correctly reported
"""

from werkzeug.security import generate_password_hash
from web import db
from web.api.models import User, QuizResult


def create_user(app, username, email):
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


def add_quiz_answers(app, username, quiz_name, answers):
    with app.app_context():
        for question_index, score in answers.items():
            db.session.add(QuizResult(
                username=username,
                quiz_name=quiz_name,
                question_index=int(question_index),
                score=score
            ))
        db.session.commit()


def login(client, username):
    with client.session_transaction() as session:
        session["user"] = username


def test_matching_requires_login(client):
    response = client.get("/matching/", follow_redirects=False)
    assert response.status_code == 401


def test_no_quiz_answers_returns_empty_matches(client, app):
    create_user(app, "lonely", "111111@student.uwa.edu.au")
    login(client, "lonely")
    response = client.get("/matching/")
    assert response.status_code == 200
    assert response.get_json()["matches"] == []


def test_identical_answers_gives_100_percent_match(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    answers = {str(i): 3 for i in range(1, 11)}
    add_quiz_answers(app, "user1", "food_preferences", answers)
    add_quiz_answers(app, "user2", "food_preferences", answers)
    login(client, "user1")
    response = client.get("/matching/")
    data = response.get_json()
    assert len(data["matches"]) == 1
    assert data["matches"][0]["username"] == "user2"
    assert data["matches"][0]["match_percentage"] == 100.0


def test_opposite_answers_gives_0_percent_match(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    add_quiz_answers(app, "user1", "food_preferences", {str(i): 1 for i in range(1, 11)})
    add_quiz_answers(app, "user2", "food_preferences", {str(i): 5 for i in range(1, 11)})
    login(client, "user1")
    response = client.get("/matching/?threshold=0")
    assert response.get_json()["matches"][0]["match_percentage"] == 0.0


def test_no_overlapping_quizzes_returns_no_match(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    answers = {str(i): 3 for i in range(1, 11)}
    add_quiz_answers(app, "user1", "food_preferences", answers)
    add_quiz_answers(app, "user2", "social_energy", answers)
    login(client, "user1")
    assert client.get("/matching/").get_json()["matches"] == []


def test_users_below_threshold_not_returned(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    add_quiz_answers(app, "user1", "food_preferences", {str(i): 1 for i in range(1, 11)})
    add_quiz_answers(app, "user2", "food_preferences", {str(i): 5 for i in range(1, 11)})
    login(client, "user1")
    assert client.get("/matching/").get_json()["matches"] == []


def test_matches_sorted_highest_to_lowest(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    create_user(app, "user3", "333333@student.uwa.edu.au")
    add_quiz_answers(app, "user1", "food_preferences", {str(i): 3 for i in range(1, 11)})
    add_quiz_answers(app, "user2", "food_preferences", {str(i): 3 for i in range(1, 11)})
    add_quiz_answers(app, "user3", "food_preferences", {str(i): 4 for i in range(1, 11)})
    login(client, "user1")
    matches = client.get("/matching/?threshold=0").get_json()["matches"]
    assert len(matches) == 2
    assert matches[0]["match_percentage"] >= matches[1]["match_percentage"]


def test_custom_threshold_via_query_param(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    answers = {str(i): 3 for i in range(1, 11)}
    add_quiz_answers(app, "user1", "food_preferences", answers)
    add_quiz_answers(app, "user2", "food_preferences", answers)
    login(client, "user1")
    response = client.get("/matching/?threshold=100")
    assert response.get_json()["threshold"] == 100


def test_match_percentage_calculated_correctly(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    add_quiz_answers(app, "user1", "food_preferences", {str(i): 1 for i in range(1, 11)})
    add_quiz_answers(app, "user2", "food_preferences", {str(i): 3 for i in range(1, 11)})
    login(client, "user1")
    response = client.get("/matching/?threshold=0")
    assert response.get_json()["matches"][0]["match_percentage"] == 50.0


def test_shared_quizzes_correctly_reported(client, app):
    create_user(app, "user1", "111111@student.uwa.edu.au")
    create_user(app, "user2", "222222@student.uwa.edu.au")
    answers = {str(i): 3 for i in range(1, 11)}
    add_quiz_answers(app, "user1", "food_preferences", answers)
    add_quiz_answers(app, "user1", "social_energy", answers)
    add_quiz_answers(app, "user2", "food_preferences", answers)
    add_quiz_answers(app, "user2", "social_energy", answers)
    login(client, "user1")
    match = client.get("/matching/").get_json()["matches"][0]
    assert match["quizzes_compared"] == 2
    assert "food_preferences" in match["shared_quizzes"]
    assert "social_energy" in match["shared_quizzes"]