from .utils import login, create_client


def test_create_category():
    client = create_client()

    responnse = client.post("/api/v1/category", json={"name": "category1"})
    assert responnse.status_code == 401

    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "category1"}

    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category1"}
    )
    assert responnse.status_code == 409

    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category2"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 2, "name": "category2"}


def test_get_category():
    client = create_client()
    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "category1"}

    responnse = client.get("/api/v1/category/1")
    assert responnse.status_code == 200
    assert responnse.json() == {
        "id": 1,
        "name": "category1",
    }

def test_list_categorys():
    client = create_client()
    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "category1"}

    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category2"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 2, "name": "category2"}

    responnse = client.get("/api/v1/category")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 1,
            "name": "category1",
        },
        {
            "id": 2,
            "name": "category2",
        },
    ]

    responnse = client.get("/api/v1/category?hide_unused=true")
    assert responnse.status_code == 200
    assert responnse.json() == []

    # create an article and add category1
    responnse = client.post(
        "/api/v1/article",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"title": "123", "content": "## subtitle"},
    )
    assert responnse.status_code == 200
    responnse = client.put(
        "/api/v1/article/1/category/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert responnse.status_code == 200

    responnse = client.get("/api/v1/category?hide_unused=true")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 1,
            "name": "category1",
        },
    ]


def test_delete_category():
    client = create_client()
    jwt = login(client, "Owner", "123456")
    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category1"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 1, "name": "category1"}

    responnse = client.post(
        "/api/v1/category", headers={"Authorization": f"Bearer {jwt}"}, json={"name": "category2"}
    )
    assert responnse.status_code == 200
    assert responnse.json() == {"id": 2, "name": "category2"}

    responnse = client.get("/api/v1/category")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 1,
            "name": "category1",
        },
        {
            "id": 2,
            "name": "category2",
        },
    ]

    responnse = client.delete("/api/v1/category/1", headers={"Authorization": f"Bearer {jwt}"})
    assert responnse.status_code == 200

    responnse = client.get("/api/v1/category")
    assert responnse.status_code == 200
    assert responnse.json() == [
        {
            "id": 2,
            "name": "category2",
        },
    ]

    responnse = client.delete("/api/v1/category/1", headers={"Authorization": f"Bearer {jwt}"})
    assert responnse.status_code == 200

    responnse = client.delete("/api/v1/category/2", headers={"Authorization": f"Bearer {jwt}"})
    assert responnse.status_code == 200

    responnse = client.get("/api/v1/category")
    assert responnse.status_code == 200
    assert responnse.json() == []
