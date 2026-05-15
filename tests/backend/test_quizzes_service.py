"""
This tests the some of the logic in quizzes/service.py
    1. generate_direct_quiz_keywords assigns partial keywords when only some questions meet the threshold
    2. calculate_category_result returns the correct category when reverse scoring is applied
    3. calculate_category_result returns None when the total score does not match any category
"""

from web.quizzes.service import (
    generate_direct_quiz_keywords,
    calculate_category_result
)
from web.quizzes.definitions import QUIZZES

#Only 1 keyword should be generated as question 1 answers 5 whilst the others answer 1
def test_direct_quiz_assigns_partial_keywords():
    quiz = QUIZZES["food_preferences"]
    answers = {str(i): 1 for i in range(1, 11)}
    answers["1"] = 5
    keywords = generate_direct_quiz_keywords(quiz, answers)
    assert len(keywords) == 1

#This tests the reverse scoring system
def test_category_result_extroverted_with_reverse_scoring():
    quiz = QUIZZES["social_energy"]
    answers = {}
    for q in quiz["questions"]:
        if q.get("reverse_scored"):
            answers[str(q["question_index"])] = 1
        else:
            answers[str(q["question_index"])] = 5
    result = calculate_category_result(quiz, answers)
    assert result == "extroverted"

#This tests the category keyword and looks to get none when creating a fake quiz with impossible category scores
def test_category_result_returns_none_when_no_match():
    fake_quiz = {
        "questions": [{"question_index": 1, "reverse_scored": False}],
        "categories": [{"name": "impossible", "min_score": 100, "max_score": 200}]
    }
    result = calculate_category_result(fake_quiz, {"1": 3})
    assert result is None