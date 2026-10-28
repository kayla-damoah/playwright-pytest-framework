import allure
import pytest

pytestmark = [pytest.mark.api, allure.feature("Posts API")]

POST_FIELDS = {"userId": int, "id": int, "title": str, "body": str}


@pytest.mark.smoke
def test_get_post_returns_expected_schema(api):
    resp = api.get("/posts/1")
    assert resp.status_code == 200
    body = resp.json()
    for field, typ in POST_FIELDS.items():
        assert isinstance(body[field], typ), f"{field} should be {typ.__name__}"
    assert body["id"] == 1


def test_list_posts_returns_100(api):
    resp = api.get("/posts")
    assert resp.status_code == 200
    assert len(resp.json()) == 100


@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_filter_posts_by_user(api, user_id):
    resp = api.get("/posts", params={"userId": user_id})
    assert resp.status_code == 200
    posts = resp.json()
    assert posts, "expected at least one post"
    assert {p["userId"] for p in posts} == {user_id}


def test_create_post_echoes_payload(api):
    payload = {"title": "qa", "body": "hello", "userId": 1}
    resp = api.post("/posts", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] == 101
    assert {k: created[k] for k in payload} == payload


def test_update_post(api):
    resp = api.put("/posts/1", json={"id": 1, "title": "new", "body": "b", "userId": 1})
    assert resp.status_code == 200
    assert resp.json()["title"] == "new"


def test_delete_post(api):
    assert api.delete("/posts/1").status_code == 200


def test_missing_post_returns_404(api):
    assert api.get("/posts/99999").status_code == 404


def test_comments_belong_to_post(api):
    resp = api.get("/posts/1/comments")
    assert resp.status_code == 200
    assert all(c["postId"] == 1 for c in resp.json())
