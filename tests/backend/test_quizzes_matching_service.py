"""
This tests the matching service logic directly
    1. Returns empty dict when a user has no quiz answers
    2. Returns answers in the correct key value format
    3. Excludes the current user from the list of other users
    4. Excludes users who have not completed any quizzes
    5. Returns None when two users have no overlapping quizzes
    6. Returns 100% match when two users have identical answers
    7. Returns 0% match when two users have opposite answers
    8. Returns 50% match when two users answers are 2 apart
    9. Returns 75% match when two users answers are 1 apart
    10. Returns empty matches when the user has no quiz answers
    11. Filters out users below the matching threshold
    12. Includes users above the matching threshold in results
"""

from web.matching.service import (
    get_answers_for_user,
    get_all_other_users,
    calculate_match_percentage,
    find_matches_for_user
)
from web.api.models import User, QuizResult
from web import db
from werkzeug.security import generate_password_hash


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


def add_answers(app, username, quiz_name, answers):
    with app.app_context():
        for q_index, score in answers.items():
            db.session.add(QuizResult(
                username=username,
                quiz_name=quiz_name,
                question_index=int(q_index),
                score=score
            ))
        db.session.commit()


#This tests that a user with no quiz answers returns an empty dictionary
def test_get_answers_empty_when_no_quiz_results(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    with app.app_context():
        result = get_answers_for_user("matchuser1")
        assert result == {}


#This tests that the answers are returned in the correct format
def test_get_answers_returns_correct_format(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    add_answers(app, "matchuser1", "food_preferences", {"1": 3, "2": 4})
    with app.app_context():
        result = get_answers_for_user("matchuser1")
        assert ("food_preferences", 1) in result
        assert result[("food_preferences", 1)] == 3
        assert result[("food_preferences", 2)] == 4


#This tests that the current user is excluded from the list of other users
def test_get_all_other_users_excludes_current_user(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    create_user(app, "matchuser2", "222222@student.uwa.edu.au")
    add_answers(app, "matchuser1", "food_preferences", {"1": 3})
    add_answers(app, "matchuser2", "food_preferences", {"1": 3})
    with app.app_context():
        result = get_all_other_users("matchuser1")
        assert "matchuser1" not in result
        assert "matchuser2" in result


#This tests that users with no quiz answers are excluded
def test_get_all_other_users_excludes_users_with_no_quizzes(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    create_user(app, "matchuser2", "222222@student.uwa.edu.au")
    add_answers(app, "matchuser1", "food_preferences", {"1": 3})
    with app.app_context():
        result = get_all_other_users("matchuser1")
        assert "matchuser2" not in result


#This tests that no match percentage is returned when there are no overlapping quizzes
def test_calculate_match_no_overlap_returns_none():
    user1 = {("food_preferences", 1): 3}
    user2 = {("social_energy", 1): 3}
    percentage, shared = calculate_match_percentage(user1, user2)
    assert percentage is None
    assert shared == []


#This tests that identical answers return a 100% match
def test_calculate_match_identical_answers_100_percent():
    answers = {("food_preferences", i): 3 for i in range(1, 11)}
    percentage, shared = calculate_match_percentage(answers, answers)
    assert percentage == 100.0
    assert "food_preferences" in shared


#This tests that opposite answers return a 0% match
def test_calculate_match_opposite_answers_0_percent():
    user1 = {("food_preferences", i): 1 for i in range(1, 11)}
    user2 = {("food_preferences", i): 5 for i in range(1, 11)}
    percentage, shared = calculate_match_percentage(user1, user2)
    assert percentage == 0.0


#This tests that answers 2 apart return a 50% match
def test_calculate_match_2_apart_gives_50_percent():
    user1 = {("food_preferences", i): 1 for i in range(1, 11)}
    user2 = {("food_preferences", i): 3 for i in range(1, 11)}
    percentage, shared = calculate_match_percentage(user1, user2)
    assert percentage == 50.0


#This tests that answers 1 apart return a 75% match
def test_calculate_match_1_apart_gives_75_percent():
    user1 = {("food_preferences", i): 2 for i in range(1, 11)}
    user2 = {("food_preferences", i): 3 for i in range(1, 11)}
    percentage, shared = calculate_match_percentage(user1, user2)
    assert percentage == 75.0


#This tests that a user with no answers returns no matches
def test_find_matches_empty_when_no_answers(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    with app.app_context():
        result = find_matches_for_user("matchuser1")
        assert result == []


#This tests that users below the threshold are filtered out
def test_find_matches_filters_below_threshold(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    create_user(app, "matchuser2", "222222@student.uwa.edu.au")
    add_answers(app, "matchuser1", "food_preferences", {str(i): 1 for i in range(1, 11)})
    add_answers(app, "matchuser2", "food_preferences", {str(i): 5 for i in range(1, 11)})
    with app.app_context():
        result = find_matches_for_user("matchuser1", threshold=70)
        assert result == []


#This tests that users above the threshold are included in the matches
def test_find_matches_includes_above_threshold(app):
    create_user(app, "matchuser1", "111111@student.uwa.edu.au")
    create_user(app, "matchuser2", "222222@student.uwa.edu.au")
    answers = {str(i): 3 for i in range(1, 11)}
    add_answers(app, "matchuser1", "food_preferences", answers)
    add_answers(app, "matchuser2", "food_preferences", answers)
    with app.app_context():
        result = find_matches_for_user("matchuser1", threshold=70)
        assert len(result) == 1
        assert result[0]["username"] == "matchuser2"
        assert result[0]["match_percentage"] == 100.0