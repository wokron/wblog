def login(client, username, password):
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    jwt = data.get("access_token")
    assert jwt is not None
    return jwt
