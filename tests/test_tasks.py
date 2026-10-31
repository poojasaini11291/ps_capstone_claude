"""
Happy-path pytest tests for the Task Management REST API.
One test per acceptance criterion (AC-001 through AC-005).
Uses an in-memory SQLite database to ensure test isolation.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import Base, get_db

# ---------------------------------------------------------------------------
# In-memory SQLite override for test isolation (DD-03)
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    """Drop and recreate all tables before each test for full isolation."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# ---------------------------------------------------------------------------
# AC-001: POST /tasks creates a task and returns 201 with the task object
# ---------------------------------------------------------------------------
def test_create_task(client):
    payload = {"title": "Buy milk", "description": "Two litres", "status": "todo"}
    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "Two litres"
    assert data["status"] == "todo"
    assert isinstance(data["id"], int)


# ---------------------------------------------------------------------------
# AC-002: GET /tasks returns 200 with a JSON array (empty when no tasks)
# ---------------------------------------------------------------------------
def test_list_tasks(client):
    # Empty store
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []

    # After creating one task
    client.post("/tasks/", json={"title": "Task 1", "description": "Desc 1"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"


# ---------------------------------------------------------------------------
# AC-003: GET /tasks/{id} returns the matching task object with 200
# ---------------------------------------------------------------------------
def test_get_task(client):
    created = client.post(
        "/tasks/", json={"title": "Write tests", "description": "All 5 ACs"}
    ).json()
    task_id = created["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Write tests"
    assert data["description"] == "All 5 ACs"
    assert data["status"] == "todo"


# ---------------------------------------------------------------------------
# AC-004: PATCH /tasks/{id} updates only the supplied fields; others unchanged
# ---------------------------------------------------------------------------
def test_update_task(client):
    created = client.post(
        "/tasks/",
        json={"title": "Original title", "description": "Original desc", "status": "todo"},
    ).json()
    task_id = created["id"]

    # Patch only the status field
    response = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    # title and description must remain unchanged
    assert data["title"] == "Original title"
    assert data["description"] == "Original desc"


# ---------------------------------------------------------------------------
# AC-005: DELETE /tasks/{id} returns 204 and removes the task
# ---------------------------------------------------------------------------
def test_delete_task(client):
    created = client.post(
        "/tasks/", json={"title": "Temporary task", "description": "Will be deleted"}
    ).json()
    task_id = created["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    # Response body must be empty for 204
    assert response.content == b""

    # Task must be absent from the list
    tasks = client.get("/tasks/").json()
    assert all(t["id"] != task_id for t in tasks)
