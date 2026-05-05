from flask import jsonify, session, request
from web.matching import matching
from web.matching.service import find_matches_for_user


@matching.route("/", methods=["GET"])
def get_matches():
    username = session.get("user")

    if not username:
        return jsonify({"error": "User must be logged in to view matches."}), 401

    threshold = request.args.get("threshold", default=70, type=int)

    #This calls the matching logic in service.py
    matches = find_matches_for_user(username, threshold)

    #The final response is returned as a JSON and formatted as follows
    return jsonify({
        "username": username,
        "threshold": threshold,
        "matches": matches
    }), 200