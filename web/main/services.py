from web import db
from web.api.models import User, ProfileLike

def get_liked_usernames(username):
    likes = ProfileLike.query.filter_by(liker_username=username).all()
    return {like.liked_username for like in likes}

def has_mutual_like(user_a, user_b):
    a_likes_b = ProfileLike.query.filter_by(liker_username=user_a,liked_username=user_b).first() is not None
    b_likes_a = ProfileLike.query.filter_by(liker_username=user_b,liked_username=user_a).first() is not None
    return a_likes_b and b_likes_a


def like_user(liker_username, liked_username):
    if liker_username == liked_username:
        return {
            "success": False,
            "message": "You cannot like yourself.",
            "liked": False,
            "match": False,
            "status_code": 400
        }

    liked_user = User.query.filter_by(username=liked_username).first()
    if not liked_user:
        return {
            "success": False,
            "message": "User not found.",
            "liked": False,
            "match": False,
            "status_code": 404
        }

    existing_like = ProfileLike.query.filter_by(liker_username=liker_username,liked_username=liked_username).first()
    if not existing_like:
        new_like = ProfileLike(liker_username=liker_username,liked_username=liked_username)
        db.session.add(new_like)
        db.session.commit()

    is_match = has_mutual_like(liker_username, liked_username)

    return {
        "success": True,
        "message": "Profile liked.",
        "liked": True,
        "match": is_match,
        "status_code": 200
    }


def unlike_user(liker_username, liked_username):
    existing_like = ProfileLike.query.filter_by(liker_username=liker_username,liked_username=liked_username).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()

    return {
        "success": True,
        "message": "Profile unliked.",
        "liked": False,
        "match": False,
        "status_code": 200
    }