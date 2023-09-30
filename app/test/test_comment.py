from .utils import login, create_client


def test_create_comment():
    client = create_client()
    jwt = login(client, "Owner", "12345678")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article/1/comment",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "this is wonderful!!"},
    )
    assert response.status_code == 200
    expect = {
        "id": 1,
        "content": "this is wonderful!!",
        "commenter_name": None,
        "like": 0,
        "dislike": 0,
        "member": {
            "id": 1,
            "name": "Owner",
            "role": "Owner",
            "is_active": True,
        },
    }
    response_json = response.json()
    for k in expect:
        assert k in response_json
        assert expect[k] == response_json[k]

    response = client.post(
        "/api/v1/article/1/comment",
        json={"content": "yes this is wonderful"},
    )
    assert response.status_code == 401

    response = client.post(
        "/api/v1/article/1/comment/visitor",
        json={"content": "yes this is really wonderful"},
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/article/1/comment/visitor",
        json={"content": "yes this is really wonderful", "commenter_name": "someone"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1/comment")
    assert response.status_code == 200
    assert len(response.json()) == 2
    for comment in response.json():
        assert comment["content"] in [
            "this is wonderful!!",
            "yes this is really wonderful",
        ]
        if comment["content"] == "yes this is really wonderful":
            assert comment["member"] == None
            assert comment["commenter_name"] == "someone"


def test_update_comment():
    client = create_client()
    jwt = login(client, "Owner", "12345678")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article/1/comment",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "this is wonderful!!"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.json()["content"] == "this is wonderful!!"

    response = client.patch(
        "/api/v1/comment/1", json={"content": "this is really wonderful"}
    )
    assert response.status_code == 401

    response = client.post("/api/v1/comment/1/like")
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.json()["like"] == 1

    response = client.post("/api/v1/comment/1/dislike")
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.json()["dislike"] == 1

    response = client.patch(
        "/api/v1/comment/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "this is really wonderful"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.json()["content"] == "this is really wonderful"

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

    response = client.patch(
        "/api/v1/comment/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "this is really really wonderful"},
    )
    assert response.status_code == 403


def test_delete_comment():
    client = create_client()
    jwt = login(client, "Owner", "12345678")

    response = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "article1"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article/1/comment",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "this is wonderful!!"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article/1/comment",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "so wonderful"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/article/1/comment",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "very wonderful"},
    )
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.status_code == 200
    assert response.json()["content"] == "this is wonderful!!"

    response = client.delete("/api/v1/comment/1")
    assert response.status_code == 401

    response = client.delete(
        "/api/v1/comment/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.status_code == 404

    response = client.delete(
        "/api/v1/comment/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/comment/1")
    assert response.status_code == 404

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

    response = client.delete(
        "/api/v1/comment/2", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403

    response = client.post(
        "/api/v1/article/1/comment/visitor",
        json={"content": "i am new here", "commenter_name": "someone"},
    )

    response = client.delete(
        "/api/v1/comment/4", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 403

    response = client.post(
        "/api/v1/article/1/comment",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"content": "i am member"},
    )

    response = client.delete(
        "/api/v1/comment/5", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    jwt = login(client, "Owner", "12345678")
    response = client.delete(
        "/api/v1/comment/4", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/comment/4")
    assert response.status_code == 404

    response = client.get("/api/v1/comment/2")
    assert response.status_code == 200

    response = client.get("/api/v1/comment/3")
    assert response.status_code == 200

    response = client.patch(
        "/api/v1/article/1",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"is_deleted": True},
    )
    assert response.status_code == 200

    response = client.delete(
        "/api/v1/article/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200

    response = client.get("/api/v1/article/1")
    assert response.status_code == 404

    response = client.get("/api/v1/comment/2")
    assert response.status_code == 404

    response = client.get("/api/v1/comment/3")
    assert response.status_code == 404
