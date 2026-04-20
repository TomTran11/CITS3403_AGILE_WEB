from flask import Blueprint

quizzes = Blueprint("quizzes", __name__)

from web.quizzes import routes