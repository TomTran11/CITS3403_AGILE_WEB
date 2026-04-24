from flask import jsonify, request, session
from web.quizzes import quizzes
from web.quizzes.service import get_quiz_names, get_quiz_by_name, save_quiz_answers


@quizzes.route("/", methods=["GET"])
def list_quizzes():
    return jsonify({
        "quizzes": get_quiz_names()
    })


@quizzes.route("/<quiz_name>", methods=["GET"])
def get_quiz(quiz_name):
    quiz = get_quiz_by_name(quiz_name)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify(quiz)


@quizzes.route("/<quiz_name>/submit", methods=["POST"])
def submit_quiz(quiz_name):
    username = session.get("user")

    if not username:
        return jsonify({"error": "User must be logged in to submit quiz."}), 401

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