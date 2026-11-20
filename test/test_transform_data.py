from etl_pipeline.transform_data import flatten_users, transform_posts

def test_flatten_users():
    users = [
        {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {"city": "Gwenborough"},
            "company": {"name": "Romaguera-Crona"},
        }
    ]
    flattened = flatten_users(users)
    assert flattened[1]["city"] == "Gwenborough"
    assert flattened[1]["company_name"] == "Romaguera-Crona"


def test_transform_posts_status_rule():
    user_lookup = {
        1: {
            "user_name": "Leanne Graham",
            "username": "Bret",
            "user_email": "Sincere@april.biz",
            "city": "Gwenborough",
            "company_name": "Romaguera-Crona",
        }
    }
    posts = [
        {"id": 1, "userId": 1, "title": "T1", "body": "a" * 150},
        {"id": 2, "userId": 1, "title": "T2", "body": "b" * 151},
    ]
    rows = transform_posts(posts, user_lookup)
    assert rows[0]["status"] == "concise"
    assert rows[1]["status"] == "lengthy"
    assert rows[1]["total_length_with_title"] == 153