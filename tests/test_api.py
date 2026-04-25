from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_unauthorized_access():
    response = client.get("/pessoa/me")
    assert response.status_code == 401

def test_not_found():
    res = client.get("/rota-invalida")
    assert res.status_code == 404

def test_auth_login_validation():
    res = client.post("/auth/login", json={})
    assert res.status_code in [400, 422]

def test_auth_register_validation():
    res = client.post("/auth/register", json={})
    assert res.status_code in [400, 422]




