from .mock import create_client
from .utils import login


def test_create_article():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200
    response_json = response.json()
    expect = {
        "id": 1,
        "title": "article1",
        "is_deleted": False,
        "category": None,
        "tags": [],
        "writer": {
            "id": 1,
            "name": "Owner",
        },
    }
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 409

    response = client.post("/api/v1/article", json={"title": "article1"})
    assert response.status_code == 401


def test_get_article():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200
    response_json = response.json()
    expect = {
        "id": 1,
        "title": "article1",
        "is_deleted": False,
        "category": None,
        "tags": [],
        "writer": {
            "id": 1,
            "name": "Owner",
        },
    }
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    response_json = response.json()
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.get("/api/v1/article/100")
    assert response.status_code == 404


def test_delete_article():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member1",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200
    jwt = login(client, "member1", "initialpassword")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200

    expect = {
        "id": 1,
        "title": "article1",
        "content": "",
        "is_deleted": False,
        "category": None,
        "tags": [],
        "writer": {
            "id": 2,
            "name": "member1",
        },
    }
    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    response_json = response.json()
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.delete("/api/v1/article/1")
    assert response.status_code == 401

    response = client.delete(
        "/api/v1/article/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403

    # one can just set article's is_deleted to True
    response = client.patch(
        "/api/v1/article/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"is_deleted": True},
    )
    assert response.status_code == 200

    # but one cannot actually delete his article
    response = client.delete(
        "/api/v1/article/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["is_deleted"] == True


def test_delete_article_by_other():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    # create common member member1
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member1",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # create manager member2
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member2",
            "role": "Manager",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # owner create article1 and set is_deleted
    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    response = client.patch(
        "/api/v1/article/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"is_deleted": True},
    )

    # manager create article2 and set is_deleted
    jwt = login(client, "member2", "initialpassword")
    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article2"},
    )
    response = client.patch(
        "/api/v1/article/2",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"is_deleted": True},
    )

    # manager cannot delete article1
    response = client.delete(
        "/api/v1/article/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403

    # common member create article3 and set is_deleted
    jwt = login(client, "member1", "initialpassword")
    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article3"},
    )
    response = client.patch(
        "/api/v1/article/3",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"is_deleted": True},
    )

    # common member cannot delete article 1 and 2
    response = client.delete(
        "/api/v1/article/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403
    response = client.delete(
        "/api/v1/article/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403

    # manager can delete article 3
    jwt = login(client, "member2", "initialpassword")
    response = client.delete(
        "/api/v1/article/3", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    # owner can delete article 2 and 1
    jwt = login(client, "Owner", "123456")
    response = client.delete(
        "/api/v1/article/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200
    response = client.delete(
        "/api/v1/article/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200


def test_update_article():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    expect = {
        "id": 1,
        "title": "article1",
        "content": "",
        "is_deleted": False,
        "category": None,
        "tags": [],
        "writer": {
            "id": 1,
            "name": "Owner",
        },
    }
    response_json = response.json()
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.patch(
        "/api/v1/article/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "new_title", "content": "new content"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    expect = {
        "id": 1,
        "title": "new_title",
        "content": "new content",
        "is_deleted": False,
        "category": None,
        "tags": [],
        "writer": {
            "id": 1,
            "name": "Owner",
        },
    }
    response_json = response.json()
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.patch(
        "/api/v1/article/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"is_deleted": True},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["is_deleted"] == True


def test_set_article_category():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/category",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"name": "c1"},
    )
    assert response.status_code == 200
    response = client.post(
        "/api/v1/category",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"name": "c2"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "a1"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["category"] == None

    response = client.put(
        "/api/v1/article/1/category/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["category"]["id"] == 1

    response = client.put(
        "/api/v1/article/1/category/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["category"]["id"] == 1

    response = client.put(
        "/api/v1/article/1/category/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["category"]["id"] == 2

    response = client.delete(
        "/api/v1/category/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["category"] == None


def test_add_article_tag():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/tag",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"name": "t1"},
    )
    assert response.status_code == 200
    response = client.post(
        "/api/v1/tag",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"name": "t2"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "a1"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == []

    response = client.put(
        "/api/v1/article/1/tag/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == [
        {
            "id": 1,
            "name": "t1",
        }
    ]

    response = client.put(
        "/api/v1/article/1/tag/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == [
        {
            "id": 1,
            "name": "t1",
        }
    ]

    response = client.put(
        "/api/v1/article/1/tag/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == [
        {
            "id": 1,
            "name": "t1",
        },
        {
            "id": 2,
            "name": "t2",
        },
    ]


def test_remove_article_tag():
    client = create_client()
    jwt = login(client, "Owner", "123456")

    response = client.post(
        "/api/v1/tag",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"name": "t1"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "a1"},
    )
    assert response.status_code == 200

    response = client.put(
        "/api/v1/article/1/tag/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == [
        {
            "id": 1,
            "name": "t1",
        }
    ]

    response = client.delete(
        "/api/v1/tag/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == []

    # delete twice
    response = client.delete(
        "/api/v1/tag/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == []

    # delete not exist
    response = client.delete(
        "/api/v1/tag/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    response = client.get("/api/v1/article/1")
    assert response.status_code == 200
    assert response.json()["title"] == "a1"
    assert response.json()["tags"] == []
