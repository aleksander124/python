from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/users/", json={"username": "testuser", "email": "test@example.com"})
    try:
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
        assert response.json()["email"] == "test@example.com"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and JSON data to match, got status_code={response.status_code}, json={response.json()}"

def test_read_user():
    response = client.get("/api/users/1")
    try:
        assert response.status_code == 200
        assert response.json()["user_id"] == 1
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and user_id=1, got status_code={response.status_code}, json={response.json()}"

def test_read_users():
    response = client.get("/api/users/")
    try:
        assert response.status_code == 200
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200, got status_code={response.status_code}"

def test_update_user():
    response = client.put("/api/users/1", json={"username": "updateduser", "email": "updated@example.com"})
    try:
        assert response.status_code == 200
        assert response.json()["username"] == "updateduser"
        assert response.json()["email"] == "updated@example.com"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and updated JSON data, got status_code={response.status_code}, json={response.json()}"

def test_delete_user():
    response = client.delete("/api/users/1")
    try:
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and message='User deleted successfully', got status_code={response.status_code}, json={response.json()}"
