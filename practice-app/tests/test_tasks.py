import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    store.reset()
    yield
    store.reset()


def test_list_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_filtered_by_done():
    client.post("/tasks", json={"title": "Open task"})
    done_task = client.post("/tasks", json={"title": "Closed task"}).json()
    client.patch(f"/tasks/{done_task['id']}", json={"done": True})

    response = client.get("/tasks", params={"done": True})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Closed task"

    response = client.get("/tasks", params={"done": False})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Open task"


def test_list_filtered_by_done_rejects_invalid_value():
    response = client.get("/tasks", params={"done": "maybe"})
    assert response.status_code == 422


def test_create_task():
    response = client.post("/tasks", json={"title": "Learn Docker"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Learn Docker"
    assert body["done"] is False
    assert body["id"] == 1


def test_create_task_rejects_empty_title():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_get_task():
    created = client.post("/tasks", json={"title": "Write CI pipeline"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Write CI pipeline"


def test_get_missing_task_returns_404():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task():
    created = client.post("/tasks", json={"title": "Ship it"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True
    assert response.json()["title"] == "Ship it"


def test_delete_task():
    created = client.post("/tasks", json={"title": "Temporary"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_missing_task_returns_404():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
