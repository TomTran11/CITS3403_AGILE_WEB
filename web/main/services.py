
from web.api.models import SocialLink
from web import db

# user = user table object, form_data = dict of form data
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

# platform = string of platform, raw = raw input from form
# returns normalised link or username, raises ValueError if invalid
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
            raise ValueError("Instagram must be a valid Instagram profile link or username")

    elif platform == "linkedin":
        if not value.startswith("http"):
            value = f"https://www.linkedin.com/in/{value}"

        if not (
            value.startswith("https://www.linkedin.com/in/")
            or value.startswith("https://www.linkedin.com/company/")
        ):
            raise ValueError("LinkedIn must be a valid LinkedIn profile or company link")

    elif platform == "discord":
        if len(value) > 50:
            raise ValueError("Discord username is too long")

    return value

# user = user table object, platform = string of platform to delete
# returns True if deleted, False if not found, raises ValueError if invalid platform
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