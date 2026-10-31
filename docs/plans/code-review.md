# Code Review

## 1. Document Details

| Field          | Value |
|----------------|-------|
| JIRA Story     | KAN-31 |
| Project        | Task Management REST API |
| Workflow ID    | WF-2026-004 |
| Reviewed by    | Code Reviewer Agent |
| Date           | 2026-11-01 |
| Branch         | feature/KAN-31-task-management-api |
| Latest Commit  | ac99149 |
| Input — Requirements    | docs/plans/requirements.md (APPROVED) |
| Input — Implementation Plan | docs/plans/impl-plan.md (APPROVED) |
| Status         | APPROVED — No BLOCKER or MAJOR findings |

---

## 2. Review Scope

Files reviewed:

| File | Purpose |
|------|---------|
| `src/database.py` | SQLAlchemy engine, session factory, Base, get_db dependency |
| `src/models.py` | ORM model for the tasks table |
| `src/schemas.py` | Pydantic v2 request/response models and status enum |
| `src/crud.py` | All five database operations |
| `src/routers/tasks.py` | FastAPI APIRouter with five HTTP endpoints |
| `src/main.py` | Application entry point |
| `tests/test_tasks.py` | Happy-path pytest test suite |
| `requirements.txt` | Runtime and test dependencies |

---

## 3. Requirements Compliance

### 3.1 Functional Requirements

| FR | Description | Status | Evidence |
|----|-------------|--------|----------|
| FR-001 | Create task with title, description, status | PASS | `POST /` in `routers/tasks.py`; `crud.create_task`; `TaskCreate` schema |
| FR-002 | Return list of all tasks | PASS | `GET /` in `routers/tasks.py`; `crud.get_tasks` |
| FR-003 | Return single task by ID | PASS | `GET /{task_id}` in `routers/tasks.py`; `crud.get_task` |
| FR-004 | Partially update a task | PASS | `PATCH /{task_id}` in `routers/tasks.py`; `crud.update_task` with `model_dump(exclude_unset=True)` |
| FR-005 | Delete a task by ID | PASS | `DELETE /{task_id}` in `routers/tasks.py`; `crud.delete_task` |

All 5 functional requirements are correctly implemented.

### 3.2 Acceptance Criteria

| AC | Description | Status | Test | Evidence |
|----|-------------|--------|------|----------|
| AC-001 | POST /tasks → 201 + task object with id | PASS | `test_create_task` | `status_code=201`, `response_model=TaskResponse`; response asserts id, title, description, status |
| AC-002 | GET /tasks → 200 + JSON array (empty when empty) | PASS | `test_list_tasks` | Returns `[]` on empty; returns 1-element array after insert |
| AC-003 | GET /tasks/{id} → 200 + matching task | PASS | `test_get_task` | Retrieves by id; asserts all fields match |
| AC-004 | PATCH /tasks/{id} → 200; only supplied fields updated | PASS | `test_update_task` | Only `status` patched; title and description verified unchanged |
| AC-005 | DELETE /tasks/{id} → 204 + task removed | PASS | `test_delete_task` | Returns 204; asserts `response.content == b""`; task absent from list |

All 5 acceptance criteria are met.

### 3.3 Non-Functional Requirements

| NFR | Requirement | Status |
|-----|-------------|--------|
| NFR-001 | Python + FastAPI | PASS |
| NFR-002 | SQLite persistence via SQLAlchemy | PASS |
| NFR-003 | JSON responses | PASS — FastAPI serialises all responses via Pydantic |
| NFR-004 | Locally runnable, no external infrastructure | PASS |

### 3.4 Design Review Notes

| Note | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| N-01 | `crud.update_task` must use `model_dump(exclude_unset=True)` | PASS | `crud.py` line 32: `for field, value in task_in.model_dump(exclude_unset=True).items()` |
| N-02 | DELETE endpoint must return `Response(status_code=204)` explicitly | PASS | `routers/tasks.py` line 45: `return Response(status_code=204)` |

Both critical design review notes are satisfied exactly as specified.

---

## 4. File-by-File Findings

### 4.1 `src/database.py`

No issues. The file correctly provides `engine`, `SessionLocal`, `Base`, and `get_db()`. The `connect_args={"check_same_thread": False}` setting is required for SQLite under FastAPI's threaded request model. The `get_db()` generator closes the session in `finally`, ensuring cleanup on both success and error paths.

### 4.2 `src/models.py`

**Finding CR-001** — MINOR

`status` column uses Python-side `default="todo"` rather than `server_default="todo"` as stated in the implementation plan (TASK-05). For this application there is no functional difference — `create_task` in `crud.py` always explicitly passes `status=task_in.status` (which defaults to `"todo"` in the `TaskCreate` schema) — but the implementation deviates from the documented spec.

No other issues. Columns match the data model: `id` (Integer, PK, autoincrement), `title` (String(255), not null), `description` (String, not null), `status` (String(20), not null).

### 4.3 `src/schemas.py`

No issues. `StatusEnum` as `Literal["todo", "in_progress", "done"]` correctly enforces assumption A-02. `TaskCreate` requires title and description with optional defaulted status. `TaskUpdate` makes all fields optional, enabling partial update. `TaskResponse` includes `ConfigDict(from_attributes=True)` for ORM-to-Pydantic conversion.

### 4.4 `src/crud.py`

No issues. All five functions are correctly implemented:

- `create_task`: Inserts, commits, refreshes, returns persisted object.
- `get_tasks`: Returns all rows.
- `get_task`: Filters by id, returns first or None.
- `update_task`: **N-01 satisfied** — uses `model_dump(exclude_unset=True)`; setattr loop applies only supplied fields; commits and refreshes.
- `delete_task`: Fetches, deletes, commits, returns the deleted object (used by the router for 404 detection).

No raw SQL, no injection risk. Uses SQLAlchemy ORM parameterisation throughout.

### 4.5 `src/routers/tasks.py`

No issues. All five endpoints are correctly defined with the required decorators, status codes, and response models. The `Response` import is present. N-02 is satisfied on line 45.

The 404 `HTTPException` on not-found paths is appropriate and required for the happy-path test that verifies task removal.

### 4.6 `src/main.py`

No issues. The import order is correct: `from src.routers.tasks import router as tasks_router` (line 4) transitively imports `models.py`, registering the `Task` model with `Base` before `Base.metadata.create_all(bind=engine)` is called (line 7). The router is registered with the correct `/tasks` prefix and `"tasks"` tag.

**Finding CR-002** — MINOR

`Base.metadata.create_all(bind=engine)` executes at module import time rather than inside a startup event or lifespan context manager. When tests import `src.main`, this call runs and creates `tasks.db` on disk as a side effect, even though tests use an in-memory override. The file is covered by `*.db` in `.gitignore` and is not used by any test, so there is no functional or security impact. Consider moving `create_all` into a FastAPI lifespan function in a future iteration to avoid the side-effect import.

### 4.7 `tests/test_tasks.py`

No issues with test correctness. All five acceptance criteria have dedicated test functions with appropriate assertions.

**Finding CR-003** — MINOR

`override_get_db()` calls `Base.metadata.create_all(bind=test_engine)` on every injected database session. The `reset_db` autouse fixture already manages the schema lifecycle (drop + create before each test). The `create_all` inside the override is therefore redundant. It is harmless but marginally wasteful; removing it would simplify the override function.

**Finding CR-004** — INFO

`app.dependency_overrides[get_db] = override_get_db` is set at module level (outside any fixture). This permanently replaces the dependency for the lifetime of the test process. This is acceptable for a single-file test suite targeting a single app instance, but it would be safer to scope the override inside a fixture for larger test suites.

**Finding CR-005** — INFO

`httpx` and `pytest` in `requirements.txt` carry no version lower bounds. For the local-only scope of this project this is acceptable. A future production deployment would benefit from pinned versions to ensure reproducibility.

---

## 5. Security Observations

| Area | Finding |
|------|---------|
| SQL injection | No risk — SQLAlchemy ORM with parameterised queries throughout; no raw SQL |
| Hardcoded secrets | None present |
| Database URL | `sqlite:///./tasks.db` — local file path, no credentials |
| Authentication | None — expected; A-04 explicitly excludes auth from scope |
| Input validation | Pydantic validates all request bodies; `StatusEnum` rejects invalid status values |

No security issues found within the defined project scope.

---

## 6. Findings Summary

| ID | File | Severity | Description |
|----|------|----------|-------------|
| CR-001 | `src/models.py` | MINOR | `status` column uses Python-side `default` instead of `server_default` as specified in the plan |
| CR-002 | `src/main.py` | MINOR | `create_all` runs at module import time, creating `tasks.db` as a side effect of test imports |
| CR-003 | `tests/test_tasks.py` | MINOR | `override_get_db` redundantly calls `create_all` on every request; `reset_db` fixture already manages the schema |
| CR-004 | `tests/test_tasks.py` | INFO | Module-level dependency override is permanent for the test process; acceptable for single-file suite |
| CR-005 | `requirements.txt` | INFO | `httpx` and `pytest` carry no version bounds; acceptable for local use |

**Blockers**: 0
**Major**: 0
**Minor**: 3
**Info**: 2

---

## 7. Overall Assessment

**APPROVED — Ready to proceed to Verification.**

The implementation fully satisfies all 5 functional requirements (FR-001 through FR-005), all 5 acceptance criteria (AC-001 through AC-005), and both critical design review notes (N-01: `model_dump(exclude_unset=True)` and N-02: explicit `Response(status_code=204)`). The code is simple, readable, and well-structured. No BLOCKER or MAJOR findings were identified. The three MINOR findings are low-risk deviations that do not affect correctness or the happy-path test suite.

---

## 8. Approval Status

**Status**: APPROVED

Reviewed by: Code Reviewer Agent
Date: 2026-11-01
JIRA Story: KAN-31
Workflow ID: WF-2026-004
