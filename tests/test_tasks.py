import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


# FR-001: Create a task with all fields
def test_create_task():
    response = client.post("/tasks/", json={
        "title": "Buy groceries",
        "description": "Milk, bread, eggs",
        "status": "todo",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, bread, eggs"
    assert data["status"] == "todo"
    assert "id" in data
    assert isinstance(data["id"], int)


# FR-001: Default status is "todo" when not provided
def test_create_task_default_status():
    response = client.post("/tasks/", json={
        "title": "Read a book",
        "description": "Read Clean Code",
    })
    assert response.status_code == 201
    assert response.json()["status"] == "todo"


# FR-002: View all tasks returns full list
def test_get_all_tasks():
    client.post("/tasks/", json={"title": "Task 1", "description": "Desc 1"})
    client.post("/tasks/", json={"title": "Task 2", "description": "Desc 2"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


# FR-002: Empty list when no tasks exist
def test_get_all_tasks_empty():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


# FR-003: View a task by ID
def test_get_task_by_id():
    created = client.post("/tasks/", json={"title": "Task A", "description": "Desc A"})
    task_id = created.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task A"


# FR-004: Partial update — only supplied fields change
def test_update_task_status_only():
    created = client.post("/tasks/", json={
        "title": "Original title",
        "description": "Original desc",
        "status": "todo",
    })
    task_id = created.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["title"] == "Original title"
    assert data["description"] == "Original desc"


# FR-004: Partial update — title only
def test_update_task_title_only():
    created = client.post("/tasks/", json={"title": "Old", "description": "Desc", "status": "todo"})
    task_id = created.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": "New"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"
    assert response.json()["status"] == "todo"


# FR-005: Delete a task
def test_delete_task():
    created = client.post("/tasks/", json={"title": "To delete", "description": "Desc"})
    task_id = created.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert f"Task with ID {task_id} has been deleted" in response.json()["message"]


# FR-005: Task is gone after deletion
def test_deleted_task_not_found():
    created = client.post("/tasks/", json={"title": "Gone", "description": "Desc"})
    task_id = created.json()["id"]
    client.delete(f"/tasks/{task_id}")
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


# FR-006: IDs are auto-incremented
def test_auto_increment_id():
    resp1 = client.post("/tasks/", json={"title": "T1", "description": "D1"})
    resp2 = client.post("/tasks/", json={"title": "T2", "description": "D2"})
    assert resp2.json()["id"] == resp1.json()["id"] + 1


# FR-007: Invalid status value is rejected with 422
def test_invalid_status_rejected():
    response = client.post("/tasks/", json={
        "title": "Bad task",
        "description": "Desc",
        "status": "invalid_status",
    })
    assert response.status_code == 422


# FR-007: Invalid status on PATCH is rejected
def test_invalid_status_on_update_rejected():
    created = client.post("/tasks/", json={"title": "Task", "description": "Desc"})
    task_id = created.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "unknown"})
    assert response.status_code == 422


# FR-008: GET non-existent task returns 404 with message
def test_get_nonexistent_task():
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert "Task with ID 9999 does not exist" in response.json()["detail"]


# FR-008: PATCH non-existent task returns 404 with message
def test_update_nonexistent_task():
    response = client.patch("/tasks/9999", json={"title": "Updated"})
    assert response.status_code == 404
    assert "Task with ID 9999 does not exist" in response.json()["detail"]


# FR-008: DELETE non-existent task returns 404 with message
def test_delete_nonexistent_task():
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    assert "Task with ID 9999 does not exist" in response.json()["detail"]
