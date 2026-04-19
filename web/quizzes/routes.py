from flask import jsonify
from web.quizzes import quizzes
from web.quizzes.definitions import QUIZZES

@quizzes.route("/", methods=["GET"])
def list_quizzes():
    return jsonify({
        "quizzes": list(QUIZZES.keys())
    })


@quizzes.route("/<quiz_name>", methods=["GET"])
def get_quiz(quiz_name):
    quiz = QUIZZES.get(quiz_name)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify(quiz)