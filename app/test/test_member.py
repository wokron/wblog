from .mock import client

jwt: str

def test_login():
    response = client.post("/token", data={"username": "Owner", "password": "123456"})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    jwt = data["access_token"]
    assert jwt is not None
