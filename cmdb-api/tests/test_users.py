# tests/test_users.py
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_read_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

def test_read_users():
    response = client.get("/api/users/")
    assert response.status_code == 200

def test_update_user():
    response = client.put("/api/users/1", json={"username": "updateduser", "email": "updated@example.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"
    assert response.json()["email"] == "updated@example.com"

def test_delete_user():
    response = client.delete("/api/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
