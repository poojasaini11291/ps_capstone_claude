# Implementation Plan

## 1. Document Details

| Field         | Value |
|---------------|-------|
| JIRA Story    | KAN-31 |
| Project       | Task Management REST API |
| Workflow ID   | WF-2026-004 |
| Prepared by   | Branch-Git-Planner Agent |
| Date          | 2026-11-01 |
| Input — Requirements | docs/plans/requirements.md (APPROVED) |
| Input — Architecture | docs/plans/architecture.md (APPROVED) |
| Input — Design Review | docs/plans/design-review.md (APPROVED — No changes required) |
| Status        | APPROVED |

---

## 2. Git Branch

**Branch name**: `feature/KAN-31-task-management-api`

Create from `main`:

```
git checkout main
git pull origin main
git checkout -b feature/KAN-31-task-management-api
```

---

## 3. Ordered Implementation Tasks

Tasks are listed in dependency order — foundation files first, application logic second, tests last.

### TASK-01 — Create `requirements.txt`

| Field | Value |
|-------|-------|
| File | `requirements.txt` |
| Depends on | Nothing |
| Purpose | Pin all runtime and test dependencies |

Contents:
```
fastapi
uvicorn[standard]
sqlalchemy
httpx
pytest
```

**Note**: Pin to versions that satisfy Python 3.10+ and are mutually compatible. No version pinning is mandated by the requirements, so latest stable versions are acceptable for this local-only service.

---

### TASK-02 — Create `src/__init__.py`

| Field | Value |
|-------|-------|
| File | `src/__init__.py` |
| Depends on | Nothing (empty file) |
| Purpose | Mark `src/` as a Python package so its modules are importable |

Contents: empty file.

---

### TASK-03 — Create `src/routers/__init__.py`

| Field | Value |
|-------|-------|
| File | `src/routers/__init__.py` |
| Depends on | TASK-02 |
| Purpose | Mark `src/routers/` as a Python package |

Contents: empty file.

---

### TASK-04 — Create `src/database.py`

| Field | Value |
|-------|-------|
| File | `src/database.py` |
| Depends on | TASK-02 |
| Purpose | SQLAlchemy engine, SessionLocal factory, Base, and get_db dependency |

Must provide:
- `engine` — SQLAlchemy engine pointing to `tasks.db` in the project root.
- `SessionLocal` — sessionmaker factory bound to `engine`.
- `Base` — declarative base for ORM model registration.
- `get_db()` — generator function used as a FastAPI `Depends` target; yields a `Session` and closes it after the request.

---

### TASK-05 — Create `src/models.py`

| Field | Value |
|-------|-------|
| File | `src/models.py` |
| Depends on | TASK-04 (`Base` from `database.py`) |
| Purpose | SQLAlchemy ORM model for the `tasks` table |

Must define:
- Class `Task` mapped to table `tasks`.
- Columns: `id` (Integer, primary key, autoincrement), `title` (String, not null), `description` (String, not null), `status` (String, not null, server_default `"todo"`).

---

### TASK-06 — Create `src/schemas.py`

| Field | Value |
|-------|-------|
| File | `src/schemas.py` |
| Depends on | TASK-02 (package exists) |
| Purpose | Pydantic v2 request/response models and status enum |

Must define:
- `StatusEnum` — `Literal["todo", "in_progress", "done"]` (enforces A-02).
- `TaskCreate` — fields: `title: str` (required), `description: str` (required), `status: StatusEnum = "todo"` (optional, defaults to `"todo"`).
- `TaskUpdate` — fields: `title: Optional[str] = None`, `description: Optional[str] = None`, `status: Optional[StatusEnum] = None` (all optional, supports PATCH partial update, AC-004).
- `TaskResponse` — fields: `id: int`, `title: str`, `description: str`, `status: str`. Configured with `model_config = ConfigDict(from_attributes=True)` for ORM-to-Pydantic conversion.

---

### TASK-07 — Create `src/crud.py`

| Field | Value |
|-------|-------|
| File | `src/crud.py` |
| Depends on | TASK-05 (`models.Task`), TASK-06 (`schemas.TaskCreate`, `schemas.TaskUpdate`) |
| Purpose | All five database operations; no HTTP or business logic |

Must implement:

| Function | Signature | Behaviour |
|----------|-----------|-----------|
| `create_task` | `(db: Session, task_in: TaskCreate) -> Task` | Insert a new Task row; commit; refresh; return the persisted object. |
| `get_tasks` | `(db: Session) -> list[Task]` | Return all rows from `tasks`. |
| `get_task` | `(db: Session, task_id: int) -> Task or None` | Return row with matching id, or `None`. |
| `update_task` | `(db: Session, task_id: int, task_in: TaskUpdate) -> Task or None` | Fetch existing task; apply only the fields present in `task_in.model_dump(exclude_unset=True)`; commit; refresh; return updated object. |
| `delete_task` | `(db: Session, task_id: int) -> Task or None` | Fetch existing task; delete it; commit; return the deleted object. |

**Critical note (N-01 from design review)**: `crud.update_task` MUST use `task_in.model_dump(exclude_unset=True)` to iterate over only the fields that were actually supplied in the PATCH request body. Iterating over all fields and checking `None` would incorrectly skip intentional `None` values and would not satisfy AC-004 partial-update semantics.

---

### TASK-08 — Create `src/routers/tasks.py`

| Field | Value |
|-------|-------|
| File | `src/routers/tasks.py` |
| Depends on | TASK-04 (`get_db`), TASK-06 (`schemas`), TASK-07 (`crud`) |
| Purpose | APIRouter defining all five HTTP endpoints |

Must implement:

| Endpoint | Decorator | Returns | Status Code |
|----------|-----------|---------|-------------|
| Create task | `@router.post("/", response_model=TaskResponse, status_code=201)` | `TaskResponse` | 201 Created |
| List tasks | `@router.get("/", response_model=list[TaskResponse])` | `list[TaskResponse]` | 200 OK |
| Get task | `@router.get("/{task_id}", response_model=TaskResponse)` | `TaskResponse` | 200 OK |
| Update task | `@router.patch("/{task_id}", response_model=TaskResponse)` | `TaskResponse` | 200 OK |
| Delete task | `@router.delete("/{task_id}", status_code=204)` | `Response` | 204 No Content |

**Critical note (N-02 from design review)**: The DELETE endpoint MUST return `Response(status_code=204)` explicitly using `from fastapi import Response`. Returning `None` or the deleted ORM object will cause FastAPI to serialise it as JSON (or `null`), producing an incorrect response body. `status_code=204` in the decorator alone is not sufficient without an explicit `Response` return.

The router must be instantiated with `router = APIRouter()` (no prefix — the prefix `/tasks` is applied in `main.py` at registration time, per ADD-08).

---

### TASK-09 — Create `src/main.py`

| Field | Value |
|-------|-------|
| File | `src/main.py` |
| Depends on | TASK-04 (`database`), TASK-05 (`models`), TASK-08 (`tasks` router) |
| Purpose | FastAPI application entry point |

Must:
- Create a `FastAPI()` instance (`app`).
- Import `Base` and `engine` from `database`; call `Base.metadata.create_all(bind=engine)` to create the `tasks` table on startup.
- Import the tasks `APIRouter` from `src.routers.tasks` and register it with `app.include_router(router, prefix="/tasks", tags=["tasks"])`.
- Export `app` so Uvicorn can reference it as `src.main:app`.

---

### TASK-10 — Create `tests/test_tasks.py`

| Field | Value |
|-------|-------|
| File | `tests/test_tasks.py` |
| Depends on | TASK-04 (`database`), TASK-05 (`models`), TASK-09 (`app`) — all application code must exist first |
| Purpose | Pytest happy-path test suite, one test per acceptance criterion |

Must:
- Override the `get_db` dependency with an in-memory SQLite engine (`sqlite:///:memory:`) so tests leave no files on disk (ADD-07, DD-03).
- Use FastAPI's `TestClient` (backed by HTTPX) for all HTTP calls.
- Define one test function per acceptance criterion:

| Test function | AC covered | What it asserts |
|---------------|------------|-----------------|
| `test_create_task` | AC-001 | POST /tasks with valid body → 201 + response body contains `id`, `title`, `description`, `status`. |
| `test_list_tasks` | AC-002 | GET /tasks on empty store → 200 + `[]`; after creating one task → 200 + array of length 1. |
| `test_get_task` | AC-003 | Create a task, then GET /tasks/{id} → 200 + matching task object. |
| `test_update_task` | AC-004 | Create a task, PATCH /tasks/{id} with only `status` changed → 200; verify only `status` changed and `title`/`description` unchanged. |
| `test_delete_task` | AC-005 | Create a task, DELETE /tasks/{id} → 204 No Content; verify task is removed (subsequent GET returns 404 or is absent from list). |

---

## 4. File Creation Order (dependency-first)

```
1.  requirements.txt
2.  src/__init__.py
3.  src/routers/__init__.py
4.  src/database.py
5.  src/models.py
6.  src/schemas.py
7.  src/crud.py
8.  src/routers/tasks.py
9.  src/main.py
10. tests/test_tasks.py
```

This order ensures that every file's imports resolve against already-written files. No circular imports exist in this topology.

---

## 5. Test Strategy

### 5.1 Framework

- **pytest** for test discovery and execution.
- **HTTPX-backed TestClient** from `fastapi.testclient` for HTTP-level testing.
- **In-memory SQLite** (`sqlite:///:memory:`) as the test database, injected via FastAPI dependency override.

### 5.2 Isolation

Each test session starts with a fresh in-memory database. The `get_db` override creates the schema with `Base.metadata.create_all` before yielding the session. No test data bleeds between test runs and no `tasks.db` file is created.

### 5.3 Coverage Map

| AC | Test | Pass Condition |
|----|------|----------------|
| AC-001 | `test_create_task` | HTTP 201, response JSON includes non-null `id` field |
| AC-002 | `test_list_tasks` | HTTP 200, returns `[]` when empty; returns 1-element array after insert |
| AC-003 | `test_get_task` | HTTP 200, response JSON matches the created task's fields and `id` |
| AC-004 | `test_update_task` | HTTP 200, only the patched field changed; unpatched fields unchanged |
| AC-005 | `test_delete_task` | HTTP 204, no response body (or empty body); task absent on subsequent check |

### 5.4 Execution Command

```bash
pytest tests/test_tasks.py -v
```

All five tests must pass before the PR is prepared.

---

## 6. Gitignore Verification

**Status: CONFIRMED COVERED**

The `.gitignore` file already contains `*.db` (line 9), which covers `tasks.db`. No change to `.gitignore` is required (N-03 from design review is satisfied).

```
# SQLite database
*.db
```

---

## 7. Key Implementation Notes (from Design Review)

| # | Note | Source | Action Required |
|---|------|--------|-----------------|
| N-01 | `crud.update_task` must use `model_dump(exclude_unset=True)` for PATCH partial-update | Design Review N-01 | Developer: iterate over `task_in.model_dump(exclude_unset=True).items()` and setattr on the ORM object |
| N-02 | DELETE endpoint must return `Response(status_code=204)` explicitly | Design Review N-02 | Developer: `from fastapi import Response`; return `Response(status_code=204)` in the delete handler |
| N-03 | `tasks.db` must not be committed | Design Review N-03 | Verified: `*.db` in `.gitignore` — no action needed |

---

## 8. Acceptance Criteria Traceability

| AC | Requirement | Implementation Task | Test |
|----|-------------|---------------------|------|
| AC-001 | FR-001 — Create task | TASK-07 (`crud.create_task`) + TASK-08 (POST /tasks) | `test_create_task` |
| AC-002 | FR-002 — List tasks | TASK-07 (`crud.get_tasks`) + TASK-08 (GET /tasks) | `test_list_tasks` |
| AC-003 | FR-003 — Get single task | TASK-07 (`crud.get_task`) + TASK-08 (GET /tasks/{id}) | `test_get_task` |
| AC-004 | FR-004 — Partial update | TASK-07 (`crud.update_task`) + TASK-08 (PATCH /tasks/{id}) | `test_update_task` |
| AC-005 | FR-005 — Delete task | TASK-07 (`crud.delete_task`) + TASK-08 (DELETE /tasks/{id}) | `test_delete_task` |

---

## 9. Approval Status

**Status**: APPROVED

Approved by: Human (explicit confirmation received 2026-11-01)

Prepared by: Branch-Git-Planner Agent
Date: 2026-11-01
JIRA Story: KAN-31
Workflow ID: WF-2026-004
