from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    r = client.post("/api/tasks/", json={"title": "Test", "description": "Desc"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test"
    assert data["status"] == "pending"


def test_list_tasks():
    client.post("/api/tasks/", json={"title": "A"})
    client.post("/api/tasks/", json={"title": "B"})
    r = client.get("/api/tasks/")
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    assert len(items) >= 2


def test_update_status():
    r = client.post("/api/tasks/", json={"title": "To Update"})
    task_id = r.json()["id"]
    u = client.patch(f"/api/tasks/{task_id}", json={"status": "done"})
    assert u.status_code == 200
    assert u.json()["status"] == "done"


