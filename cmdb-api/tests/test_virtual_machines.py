from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)

def test_create_vm():
    response = client.post("/api/virtualmachines/", json={"vm_name": "testvm", "user_id": 1, "memory_gb": 4, "cpu_cores": 2, "os_type": "linux"})
    try:
        assert response.status_code == 200
        assert response.json()["vm_name"] == "testvm"
        assert response.json()["memory_gb"] == 4
        assert response.json()["cpu_cores"] == 2
        assert response.json()["os_type"] == "linux"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and JSON data to match, got status_code={response.status_code}, json={response.json()}"

def test_read_vm():
    response = client.get("/api/virtualmachines/testvm")
    try:
        assert response.status_code == 200
        assert response.json()["vm_name"] == "testvm"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and vm_name='testvm', got status_code={response.status_code}, json={response.json()}"

def test_read_vms():
    response = client.get("/api/virtualmachines/")
    try:
        assert response.status_code == 200
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200, got status_code={response.status_code}"

def test_update_vm():
    response = client.put("/api/virtualmachines/testvm", json={"memory_gb": 8, "cpu_cores": 4, "os_type": "windows"})
    try:
        assert response.status_code == 200
        assert response.json()["memory_gb"] == 8
        assert response.json()["cpu_cores"] == 4
        assert response.json()["os_type"] == "windows"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and updated JSON data, got status_code={response.status_code}, json={response.json()}"

def test_delete_vm():
    response = client.delete("/api/virtualmachines/testvm")
    try:
        assert response.status_code == 200
        assert response.json()["message"] == "VM deleted successfully"
    except AssertionError:
        assert False, f"AssertionError: Expected status_code=200 and message='VM deleted successfully', got status_code={response.status_code}, json={response.json()}"
