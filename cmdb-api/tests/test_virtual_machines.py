# tests/test_virtual_machines.py
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_vm():
    response = client.post("/api/virtualmachines/", json={"vm_name": "testvm", "user_id": 1, "memory_gb": 4, "cpu_cores": 2, "os_type": "linux"})
    assert response.status_code == 200
    assert response.json()["vm_name"] == "testvm"
    assert response.json()["memory_gb"] == 4
    assert response.json()["cpu_cores"] == 2
    assert response.json()["os_type"] == "linux"

def test_read_vm():
    response = client.get("/api/virtualmachines/testvm")
    assert response.status_code == 200
    assert response.json()["vm_name"] == "testvm"

def test_read_vms():
    response = client.get("/api/virtualmachines/")
    assert response.status_code == 200

def test_update_vm():
    response = client.put("/api/virtualmachines/testvm", json={"memory_gb": 8, "cpu_cores": 4, "os_type": "windows"})
    assert response.status_code == 200
    assert response.json()["memory_gb"] == 8
    assert response.json()["cpu_cores"] == 4
    assert response.json()["os_type"] == "windows"

def test_delete_vm():
    response = client.delete("/api/virtualmachines/testvm")
    assert response.status_code == 200
    assert response.json()["message"] == "VM deleted successfully"
