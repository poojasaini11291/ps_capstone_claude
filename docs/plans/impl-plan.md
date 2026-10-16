
# Implementation Plan
## Task Management REST API

**Workflow ID:** WF-2026-001
**Stage:** Implementation Planning
**Author:** Branch & Git Planner Agent
**Date:** 2026-10-17
**Inputs:** docs/plans/requirements.md, docs/plans/architecture.md, docs/plans/design-review.md

---

## 1. Branch Strategy

| Item | Value |
|------|-------|
| Base branch | `main` |
| Feature branch | `feature/task-management-api` |
| Merge strategy | Single PR from feature branch into main |
| Commit style | One commit per logical task group |

---

## 2. Dependency Order

```
TASK-001 (Project Setup)
    └── TASK-002 (Database Layer)
            └── TASK-003 (Task ORM Model)
                    └── TASK-004 (Pydantic Schemas)  ← also independent, can run after TASK-001
                            └── TASK-005 (Task Router)
                                    └── TASK-006 (Application Entry Point)
                                            └── TASK-007 (Startup Verification)
```

---

## 3. Implementation Tasks

### TASK-001 — Project Setup
**Depends on:** none
**Description:** Create directory structure and dependency files.

Files to create:
- `src/` directory
- `src/routers/` directory
- `tests/` directory
- `requirements.txt`
- `requirements-test.txt`

`requirements.txt` contents:
```
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
```

`requirements-test.txt` contents:
```
pytest>=8.0.0
httpx>=0.27.0
```

---

### TASK-002 — Database Layer
**Depends on:** TASK-001
**Description:** Implement SQLite engine, session factory, declarative Base, and `get_db` dependency.

File to create: `src/database.py`

Must implement:
- `SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"`
- `engine` using `create_engine` with `connect_args={"check_same_thread": False}`
- `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`
- `Base = declarative_base()`
- `get_db()` generator that yields a session and closes it in `finally`
- `create_tables()` function that calls `Base.metadata.create_all(bind=engine)`

---

### TASK-003 — Task ORM Model
**Depends on:** TASK-002 (imports `Base` from `database.py`)
**Description:** Define the SQLAlchemy ORM model for the `tasks` table.

File to create: `src/models.py`

Must implement:
- `class Task(Base)` with `__tablename__ = "tasks"`
- `id`: `Integer`, `primary_key=True`, `index=True`, `autoincrement=True`
- `title`: `String(255)`, `nullable=False`
- `description`: `Text`, `nullable=False`
- `status`: `String(20)`, `nullable=False`, `default="todo"`

---

### TASK-004 — Pydantic Schemas
**Depends on:** TASK-001 (directory exists)
**Description:** Define request/response Pydantic models.

File to create: `src/schemas.py`

Must implement:
- `TaskCreate(BaseModel)`: `title: str`, `description: str`, `status: Literal["todo", "in_progress", "done"] = "todo"`
- `TaskUpdate(BaseModel)`: `title: Optional[str] = None`, `description: Optional[str] = None`, `status: Optional[Literal["todo", "in_progress", "done"]] = None`
- `TaskResponse(BaseModel)`: `id: int`, `title: str`, `description: str`, `status: str` — with `model_config = ConfigDict(from_attributes=True)` (Pydantic v2 style)

---

### TASK-005 — Task Router
**Depends on:** TASK-002, TASK-003, TASK-004
**Description:** Implement all 5 CRUD endpoints.

Files to create:
- `src/routers/__init__.py` (empty)
- `src/routers/tasks.py`

Endpoints to implement:

| Method | Path | Logic |
|--------|------|-------|
| POST `/tasks` | Create | Validate `TaskCreate`, insert row, return `TaskResponse` with status 201 |
| GET `/tasks` | List all | Query all rows, return `list[TaskResponse]` with status 200 |
| GET `/tasks/{id}` | Get one | Query by id; raise `HTTPException(404)` if not found; return `TaskResponse` |
| PATCH `/tasks/{id}` | Update | Fetch task (404 if missing); apply only non-None fields from `TaskUpdate`; commit; return `TaskResponse` |
| DELETE `/tasks/{id}` | Delete | Fetch task (404 if missing); delete; commit; return `{"message": "Task with ID {id} deleted successfully"}` |

404 message format: `"Task with ID {id} does not exist"`

---

### TASK-006 — Application Entry Point
**Depends on:** TASK-005
**Description:** Create the FastAPI app, include the router, and trigger table creation on startup.

File to create: `src/main.py`

Must implement:
- `app = FastAPI(title="Task Management API")`
- Import and call `create_tables()` from `database.py` at module level (before routes register)
- `app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])`

---

### TASK-007 — Startup Verification
**Depends on:** TASK-006
**Description:** Run the application and confirm it starts without errors.

Command:
```bash
cd src && uvicorn main:app --reload
```

Expected: server starts on `http://127.0.0.1:8000`, no import or DB errors logged.

Developer must confirm startup before reporting this task complete.

---

## 4. Expected Output Files

```
src/
├── main.py
├── database.py
├── models.py
├── schemas.py
└── routers/
    ├── __init__.py
    └── tasks.py
requirements.txt
requirements-test.txt
```

---

## 5. Out of Scope for Implementation

- No test files — written by automation-tester agent in Stage 7
- No `.env` file — no secrets needed for local SQLite
- No Docker or deployment config
- No authentication middleware

---

## 6. Approval Status

**Status: AWAITING HUMAN APPROVAL**

Please review the implementation plan above and confirm approval to proceed to development.
No application code will be written until approval is received.
