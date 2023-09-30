from .utils import login, create_client


def test_login():
    client = create_client()
    jwt = login(client, "Owner", "12345678")


def test_get_current_member():
    client = create_client()
    jwt = login(client, "Owner", "12345678")
    response = client.get(
        "/api/v1/member/me",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Owner",
        "role": "Owner",
        "is_active": True,
    }


def test_get_member_success():
    client = create_client()
    jwt = login(client, "Owner", "12345678")
    response = client.get(
        "/api/v1/member/1", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Owner",
        "role": "Owner",
        "is_active": True,
    }


def test_get_member_with_invalid_id():
    client = create_client()
    jwt = login(client, "Owner", "12345678")
    response = client.get(
        "/api/v1/member/100", headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 404


def test_create_member_simple():
    client = create_client()
    jwt = login(client, "Owner", "12345678")
    # create member1
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member1",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # get member1
    response = client.get(
        "/api/v1/member/2",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "member1",
        "role": "Common Member",
        "is_active": True,
    }

    # create member2
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

    # get member2
    response = client.get(
        "/api/v1/member/3",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "name": "member2",
        "role": "Manager",
        "is_active": True,
    }


def test_create_member_permission_check():
    client = create_client()
    jwt = login(client, "Owner", "12345678")
    # Onwer try to create member as Owner
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member1",
            "password": "initialpassword",
            "role": "Owner",
        },
    )
    response.status_code == 403

    # Onwer create member1
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member1",
            "role": "Manager",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # login member1
    jwt = login(client, "member1", "initialpassword")

    # Manager member1 try to create member2 as Manager
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member2",
            "role": "Manager",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 403

    # create member2 as Common Member
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member2",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # login member2
    jwt = login(client, "member2", "initialpassword")

    # Common Member member2 try to create member3 as common member
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member3",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 403


def test_update_member_simple():
    client = create_client()
    jwt = login(client, "Owner", "12345678")

    # get personal info
    response = client.get(
        "/api/v1/member/me",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Owner",
        "role": "Owner",
        "is_active": True,
    }

    # try to modify name
    response = client.patch(
        "/api/v1/member/1",
        json={"name": "OwnerNewName"},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    jwt = login(client, "OwnerNewName", "12345678")  # relogin is needed

    # get personal info again
    response = client.get(
        "/api/v1/member/me",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "OwnerNewName",
        "role": "Owner",
        "is_active": True,
    }

    # one cannot modify is_active
    response = client.patch(
        "/api/v1/member/1",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 403

    # modify password
    response = client.patch(
        "/api/v1/member/1",
        json={"password": "newpassword"},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200
    jwt = login(client, "OwnerNewName", "newpassword")  # relogin is needed


def test_update_member_by_other():
    client = create_client()
    jwt = login(client, "Owner", "12345678")

    # create manager member1
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member1",
            "role": "Manager",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # create common member member2
    response = client.post(
        "/api/v1/member",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "name": "member2",
            "password": "initialpassword",
        },
    )
    assert response.status_code == 200

    # member2 login
    jwt = login(client, "member2", "initialpassword")

    # member2 try to modify Owner
    response = client.patch(
        "/api/v1/member/1",
        json={"password": "thisismypassword"},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 403

    # member2 try to modify member1
    response = client.patch(
        "/api/v1/member/2",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 403

    # member1 login
    jwt = login(client, "member1", "initialpassword")

    # member1 try to modfiy Owner
    response = client.patch(
        "/api/v1/member/1",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 403

    # member1 forbid member2 successfully
    response = client.patch(
        "/api/v1/member/3",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {jwt}"},
    )
    assert response.status_code == 200

    # now member2 can not login anymore
    response = client.post(
        "/token", data={"username": "member2", "password": "initialpassword"}
    )
    assert response.status_code == 403
