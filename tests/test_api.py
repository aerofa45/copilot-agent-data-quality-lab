from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_lookup_customer():
    r = client.get("/customers/101")
    assert r.status_code == 200
    assert r.json()["name"] == "John Smith"

def test_create_ticket():
    r = client.post("/tickets", json={
        "customer_id": 101,
        "device_id": "DEV-100",
        "issue": "VPN connection fails",
        "severity": "normal"
    })
    assert r.status_code == 200
    assert r.json()["status"] == "open"

def test_reject_device_customer_mismatch():
    r = client.post("/tickets", json={
        "customer_id": 101,
        "device_id": "DEV-101",
        "issue": "Test",
        "severity": "normal"
    })
    assert r.status_code == 400
