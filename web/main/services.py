from web import db
from web.api.models import User, ProfileLike, Notification, SocialLink


def get_liked_usernames(username):
    likes = ProfileLike.query.filter_by(liker_username=username).all()
    return {like.liked_username for like in likes}


def has_mutual_like(user_a, user_b):
    a_likes_b = ProfileLike.query.filter_by(
        liker_username=user_a,
        liked_username=user_b
    ).first() is not None

    b_likes_a = ProfileLike.query.filter_by(
        liker_username=user_b,
        liked_username=user_a
    ).first() is not None

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

    new_like_created = False

    existing_like = ProfileLike.query.filter_by(
        liker_username=liker_username,
        liked_username=liked_username
    ).first()

    if not existing_like:
        new_like = ProfileLike(
            liker_username=liker_username,
            liked_username=liked_username
        )
        db.session.add(new_like)
        db.session.commit()
        new_like_created = True

    is_match = has_mutual_like(liker_username, liked_username)

    if is_match and new_like_created:
        liker_user = User.query.filter_by(username=liker_username).first()

        notification_for_liker = Notification(
            user_id=liker_username,
            type="match",
            message=f"You matched with {liked_user.displayname}!",
            related_user_id=liked_username
        )

        notification_for_liked = Notification(
            user_id=liked_username,
            type="match",
            message=f"You matched with {liker_user.displayname}!",
            related_user_id=liker_username
        )

        db.session.add_all([notification_for_liker, notification_for_liked])
        db.session.commit()

    return {
        "success": True,
        "message": "Profile liked.",
        "liked": True,
        "match": is_match,
        "status_code": 200
    }


def unlike_user(liker_username, liked_username):
    existing_like = ProfileLike.query.filter_by(
        liker_username=liker_username,
        liked_username=liked_username
    ).first()

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


def update_user_socials(user, form_data):
    platforms = ["instagram", "linkedin", "discord"]

    for platform in platforms:
        if platform not in form_data:
            continue

        raw = form_data.get(platform, "").strip()
        value = normalise_social_link(platform, raw)

        existing = SocialLink.query.filter_by(
            user_id=user.username,
            platform=platform
        ).first()

        if not value:
            continue

        if existing:
            existing.link = value
        else:
            db.session.add(SocialLink(
                user_id=user.username,
                platform=platform,
                link=value
            ))

    db.session.commit()


def normalise_social_link(platform, raw):
    value = raw.strip()

    if not value:
        return ""

    if platform == "instagram":
        if value.startswith("@"):
            value = value[1:]

        if not value.startswith("http"):
            value = f"https://www.instagram.com/{value}"

        if not value.startswith("https://www.instagram.com/"):
            raise ValueError(
                "Instagram must be a valid Instagram profile link or username"
            )

    elif platform == "linkedin":
        if not value.startswith("http"):
            value = f"https://www.linkedin.com/in/{value}"

        if not (
            value.startswith("https://www.linkedin.com/in/")
            or value.startswith("https://www.linkedin.com/company/")
        ):
            raise ValueError(
                "LinkedIn must be a valid LinkedIn profile or company link"
            )

    elif platform == "discord":
        if len(value) > 50:
            raise ValueError("Discord username is too long")

    return value


def delete_user_social(user, platform):
    allowed_platforms = ["instagram", "linkedin", "discord"]

    if platform not in allowed_platforms:
        raise ValueError("Invalid social platform")

    social = SocialLink.query.filter_by(
        user_id=user.username,
        platform=platform
    ).first()

    if not social:
        return False

    db.session.delete(social)
    db.session.commit()

    return True