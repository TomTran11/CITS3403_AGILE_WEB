from flask import Blueprint

matching = Blueprint("matching", __name__, url_prefix="/matching")

from web.matching import routes