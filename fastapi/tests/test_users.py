from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"user": "testuser", "passw": "testpassword", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["user"] == "testuser"