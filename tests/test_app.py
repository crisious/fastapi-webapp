"""Smoke tests for the API and the static front end."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "fastapi-webapp"


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "FastAPI Web App" in r.text


def test_openapi_docs_available():
    r = client.get("/docs")
    assert r.status_code == 200


def test_items_crud_lifecycle():
    # create
    r = client.post("/api/items", json={"title": "pytest-created item"})
    assert r.status_code == 201, r.text
    item_id = r.json()["id"]

    # read
    r = client.get(f"/api/items/{item_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "pytest-created item"

    # update
    r = client.patch(f"/api/items/{item_id}", json={"title": "pytest-created item", "done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True

    # delete
    assert client.delete(f"/api/items/{item_id}").status_code == 204
    assert client.get(f"/api/items/{item_id}").status_code == 404


def test_missing_item_404():
    assert client.get("/api/items/999999").status_code == 404
