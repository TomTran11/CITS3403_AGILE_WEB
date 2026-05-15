from flask import jsonify, request, session, render_template
from web.quizzes import quizzes
from web.quizzes.service import (get_quiz_names, get_quiz_by_name, save_quiz_answers, get_completed_quizzes_for_user, get_keywords_for_quiz)
from web.auth.utils import require_login
from web.api.models import User


@quizzes.route("/", methods=["GET"])
def list_quizzes():
    return jsonify({
        "quizzes": get_quiz_names()
    })

@quizzes.route("/page", methods=["GET"])
@require_login
def quizzes_page():
    username = username = session.get("user")
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("quizzes/quizzes.html",user=user)

@quizzes.route("/<quiz_name>", methods=["GET"])
def get_quiz(quiz_name):
    quiz = get_quiz_by_name(quiz_name)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify(quiz)

@quizzes.route("/<quiz_name>/submit", methods=["POST"])
@require_login
def submit_quiz(quiz_name):
    username = session.get("user")

    data = request.get_json()

    if not data:
        return jsonify({"error": "No quiz data received."}), 400

    answers = data.get("answers")

    success, message, keywords = save_quiz_answers(
        username=username,
        quiz_name=quiz_name,
        answers=answers
    )

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({
        "message": message,
        "quiz_name": quiz_name,
        "generated_keywords": keywords
    }), 200

@quizzes.route("/completed", methods=["GET"])
@require_login
def completed_quizzes():
    username = session.get("user")
    completed = get_completed_quizzes_for_user(username)
    return jsonify({
        "username": username,
        "completed_quizzes": completed
    }), 200

@quizzes.route("/<quiz_name>/keywords", methods=["GET"])
@require_login
def quiz_keywords(quiz_name):
    username = session.get("user")
    quiz = get_quiz_by_name(quiz_name)
    if not quiz:
        return jsonify({"error": "Quiz not found."}), 404
    keywords = get_keywords_for_quiz(username, quiz_name)
    return jsonify({
        "username": username,
        "quiz_name": quiz_name,
        "keywords": keywords
    }), 200