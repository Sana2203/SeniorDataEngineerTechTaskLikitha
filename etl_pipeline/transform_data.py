import logging

logger = logging.getLogger(__name__)


def flatten_users(users: list[dict]) -> dict[int, dict]:
    """Flatten nested user fields into a lookup dictionary keyed by user id."""
    user_lookup: dict[int, dict] = {}
    for user in users:
        user_id = user.get("id")
        if user_id is None:
            continue
        address = user.get("address") or {}
        company = user.get("company") or {}
        user_lookup[user_id] = {
            "user_name": user.get("name"),
            "username": user.get("username"),
            "user_email": user.get("email"),
            "city": address.get("city"),
            "company_name": company.get("name"),
        }
    return user_lookup


def transform_posts(posts: list[dict], user_lookup: dict[int, dict]) -> list[dict]:
    """Enrich posts with user details and compute post length and status."""
    enriched_rows: list[dict] = []
    for post in posts:
        post_id = post.get("id")
        user_id = post.get("userId")
        title = post.get("title") or ""
        body = post.get("body") or ""

        if post_id is None or user_id is None:
            logger.warning("Skipping post missing id or userId: %s", post)
            continue
        body_length = len(body)
        total_length_with_title = len(title) + body_length
        status = "lengthy" if body_length > 150 else "concise"

        user_info = user_lookup.get(user_id, {})
        if not user_info:
            logger.warning("No matching user found for user_id=%s on post_id=%s", user_id, post_id)

        enriched_rows.append({
            "post_id": post_id,
            "user_id": user_id,
            "title": title,
            "body": body,
            "body_length": body_length,
            "total_length_with_title": total_length_with_title,
            "status": status,
            "user_name": user_info.get("user_name"),
            "username": user_info.get("username"),
            "user_email": user_info.get("user_email"),
            "city": user_info.get("city"),
            "company_name": user_info.get("company_name"),
        })
    return enriched_rows