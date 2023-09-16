from .mock import create_client
from .utils import login


def test_create_tag():
    client = create_client()

    responnse = client.post("/api/v1/tag", json={"name": "tag1"})
    assert responnse.status_code == 401

    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "tag1"}

    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag1"}
    )
    assert responnse.status_code == 409

    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag2"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 2, "name": "tag2"}


def test_get_tag():
    client = create_client()
    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "tag1"}

    responnse = client.get("/api/v1/tag/1")
    assert responnse.status_code == 200
    assert responnse.json() == {
        "id": 1,
        "name": "tag1",
    }


def test_list_tags():
    client = create_client()
    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "tag1"}

    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag2"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 2, "name": "tag2"}

    responnse = client.get("/api/v1/tag")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 1,
            "name": "tag1",
        },
        {
            "id": 2,
            "name": "tag2",
        },
    ]

    responnse = client.get("/api/v1/tag?hide_unused=true")
    assert responnse.status_code == 200
    assert responnse.json() == []

    # create an article and add tag1
    responnse = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "123", "content": "## subtitle"},
    )
    assert responnse.status_code == 200
    responnse = client.post(
        "/api/v1/article/1/tag/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert responnse.status_code == 200

    responnse = client.get("/api/v1/tag?hide_unused=true")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 1,
            "name": "tag1",
        },
    ]


def test_delete_tag():
    client = create_client()
    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "tag1"}

    responnse = client.post(
        "/api/v1/tag", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "tag2"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 2, "name": "tag2"}

    responnse = client.get("/api/v1/tag")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 1,
            "name": "tag1",
        },
        {
            "id": 2,
            "name": "tag2",
        },
    ]

    responnse = client.delete("/api/v1/tag/1", headers={"Authorization": f"Bearer {jwt}"})
    assert responnse.status_code == 200

    responnse = client.get("/api/v1/tag")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 2,
            "name": "tag2",
        },
    ]

    responnse = client.delete("/api/v1/tag/1", headers={"Authorization": f"Bearer {jwt}"})
    assert responnse.status_code == 200

    responnse = client.delete("/api/v1/tag/2", headers={"Authorization": f"Bearer {jwt}"})
    assert responnse.status_code == 200

    responnse = client.get("/api/v1/tag")
    assert responnse.status_code == 200
    assert responnse.json() == []
