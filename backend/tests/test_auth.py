def register(client, email="cliente@example.com", password="ClaveSegura12"):
    return client.post("/api/v1/auth/register", json={"full_name": "Cliente de Prueba", "email": email, "password": password})


def login(client, email="cliente@example.com", password="ClaveSegura12"):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def test_register_and_login(client):
    response = register(client)
    assert response.status_code == 201
    assert response.json()["email"] == "cliente@example.com"
    response = login(client)
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["user"]["role"] == "cliente"


def test_reject_duplicate_email(client):
    assert register(client).status_code == 201
    response = register(client)
    assert response.status_code == 409
    assert "ya existe" in response.json()["detail"].lower()


def test_reject_invalid_credentials(client):
    register(client)
    response = login(client, password="Incorrecta99")
    assert response.status_code == 401


def test_protected_endpoint_requires_token(client):
    assert client.get("/api/v1/auth/me").status_code in (401, 403)
    register(client)
    token = login(client).json()["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "cliente@example.com"


def test_change_password(client):
    register(client)
    token = login(client).json()["access_token"]
    response = client.post("/api/v1/auth/change-password", headers={"Authorization": f"Bearer {token}"}, json={"current_password": "ClaveSegura12", "new_password": "NuevaClave34"})
    assert response.status_code == 204
    assert login(client).status_code == 401
    assert login(client, password="NuevaClave34").status_code == 200

