from flask import Blueprint, jsonify
from web.data.language_loader import LANGUAGE_DATA

api = Blueprint('api', __name__)

@api.route('/languages')
def get_languages():
    return jsonify({"languages": sorted(LANGUAGE_DATA)})