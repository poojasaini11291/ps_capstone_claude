# Design Review

## 1. Document Details

| Field         | Value |
|---------------|-------|
| JIRA Story    | KAN-31 |
| Project       | Task Management REST API |
| Workflow ID   | WF-2026-004 |
| Reviewed by   | Solution Engineer Agent |
| Date          | 2026-11-01 |
| Input — Requirements | docs/plans/requirements.md (APPROVED) |
| Input — Architecture | docs/plans/architecture.md (DRAFT) |
| Review Status | **APPROVED — No changes required** |

---

## 2. Review Summary

The architecture for KAN-31 (Task Management REST API) is well-structured, proportionate in scope, and fully aligned with the approved requirements. The three-layer design (FastAPI Router → CRUD → SQLAlchemy/SQLite) is appropriate for a single-process, locally-runnable REST service covering five CRUD operations. No over-engineering was identified. All five functional requirements, all five acceptance criteria, and all four non-functional requirements are traceable to specific components in the architecture.

---

## 3. Requirement Coverage

### 3.1 Functional Requirements

| Requirement | Covered By | Verdict |
|-------------|------------|---------|
| FR-001 — Create task (title, description, status) | `POST /tasks` → `TaskCreate` schema → `crud.create_task` → SQLite INSERT | COVERED |
| FR-002 — List all tasks | `GET /tasks` → `crud.get_tasks` → SQLite SELECT * | COVERED |
| FR-003 — Get single task by ID | `GET /tasks/{id}` → `crud.get_task` → SQLite SELECT WHERE id = ? | COVERED |
| FR-004 — Partially update a task | `PATCH /tasks/{id}` → `TaskUpdate` (all fields optional) → `crud.update_task` → SQLite UPDATE | COVERED |
| FR-005 — Delete task by ID | `DELETE /tasks/{id}` → `crud.delete_task` → SQLite DELETE | COVERED |

All 5 functional requirements are fully addressed.

### 3.2 Acceptance Criteria

| AC | Expected Outcome | Architecture Support | Verdict |
|----|-----------------|----------------------|---------|
| AC-001 | POST /tasks → 201 Created + task object with `id` | Router returns `status_code=201` and `TaskResponse` (which includes `id`) | ACHIEVABLE |
| AC-002 | GET /tasks → 200 OK + JSON array (empty `[]` when no tasks) | `crud.get_tasks` returns `[]` when table empty; FastAPI serialises to JSON array | ACHIEVABLE |
| AC-003 | GET /tasks/{id} → 200 OK + matching task object | `crud.get_task` returns the ORM object; router serialises via `TaskResponse` | ACHIEVABLE |
| AC-004 | PATCH /tasks/{id} → 200 OK; only supplied fields updated | `TaskUpdate` has all fields optional; `crud.update_task` applies only non-None fields | ACHIEVABLE |
| AC-005 | DELETE /tasks/{id} → 204 No Content + task removed | Router returns `status_code=204`; `crud.delete_task` removes the row (DD-06) | ACHIEVABLE |

All 5 acceptance criteria are achievable with the proposed design.

### 3.3 Non-Functional Requirements

| Requirement | Architecture Provision | Verdict |
|-------------|------------------------|---------|
| NFR-001 — Python + FastAPI | FastAPI on Python 3.10+; Uvicorn ASGI server | SATISFIED |
| NFR-002 — SQLite persistence | SQLAlchemy engine targeting `tasks.db`; no external DB | SATISFIED |
| NFR-003 — JSON responses | FastAPI + Pydantic v2 automatic JSON serialisation for all endpoints (DELETE returns no body per REST convention) | SATISFIED |
| NFR-004 — Local execution only | Uvicorn on localhost; no cloud infra, no containers, no external services | SATISFIED |

All 4 non-functional requirements are satisfied.

---

## 4. Architecture Review Findings

### 4.1 Three-Layer Design Assessment

The three-layer layout is appropriate and correctly applied:

| Layer | Component | Assessment |
|-------|-----------|------------|
| HTTP layer | `src/routers/tasks.py` (APIRouter) | Handles all five endpoints, status codes, and response serialisation. Delegates data access to CRUD. Correct separation. |
| Business/Routing layer | `src/crud.py` | Pure database operations; no HTTP concerns. Accepts `Session` as dependency. No business logic bleed. |
| Persistence layer | `src/database.py` + `src/models.py` | Engine, session factory, and `get_db` dependency correctly separated from model definition. Clean. |

The `main.py` entry point correctly handles only app instantiation, router registration, and table creation — no logic placed there.

### 4.2 Data Model Consistency

The SQLite table definition (Section 5.1 of architecture) maps exactly to the requirements data model (Section 4 of requirements):

| Field | Requirements Spec | Architecture Spec | Match |
|-------|------------------|-------------------|-------|
| id | integer, auto-incremented | INTEGER PRIMARY KEY AUTOINCREMENT | Yes |
| title | string, required | TEXT NOT NULL | Yes |
| description | string, required | TEXT NOT NULL | Yes |
| status | string, required, default `todo` | TEXT NOT NULL DEFAULT 'todo' | Yes |

### 4.3 Pydantic Schema Design

- `TaskCreate`: `title` and `description` required, `status` optional with default `"todo"` — matches A-03.
- `TaskUpdate`: all fields optional — correctly supports partial updates required by FR-004 and AC-004.
- `TaskResponse`: includes `id`; configured with `from_attributes=True` for ORM-to-Pydantic conversion — necessary and correct.
- `StatusEnum` as `Literal["todo", "in_progress", "done"]`: enforces A-02 at the API layer without adding SQLite CHECK constraints, keeping the DB schema minimal (DD-04).

### 4.4 Endpoint Specification Verification

All five endpoints in the REST API Endpoint Specification (architecture Section 6) match the requirements and data flows:

| Method + Path | Status Code | Body | FR / AC | Match |
|---------------|-------------|------|---------|-------|
| POST /tasks | 201 | TaskResponse | FR-001, AC-001 | Correct |
| GET /tasks | 200 | TaskResponse[] | FR-002, AC-002 | Correct |
| GET /tasks/{id} | 200 | TaskResponse | FR-003, AC-003 | Correct |
| PATCH /tasks/{id} | 200 | TaskResponse | FR-004, AC-004 | Correct |
| DELETE /tasks/{id} | 204 | None | FR-005, AC-005 | Correct |

### 4.5 Test Strategy Assessment

The proposed test approach is correct for the happy-path focus defined in project scope:

- In-memory SQLite override via `Depends` replacement ensures test isolation (DD-03) — no file system artefacts.
- One test per acceptance criterion (AC-001 through AC-005) is the right level of coverage for happy-path scope.
- `pytest` with `HTTPX`-backed `TestClient` is the idiomatic FastAPI testing pattern.

### 4.6 File Structure Assessment

The proposed directory structure (architecture Section 8) is complete, consistent, and appropriately minimal:

```
src/
├── __init__.py           ← Required for module imports
├── main.py               ← App entry point only
├── database.py           ← DB wiring only
├── models.py             ← ORM model only
├── schemas.py            ← Pydantic schemas only
├── crud.py               ← DB operations only
└── routers/
    ├── __init__.py       ← Required for package
    └── tasks.py          ← Endpoint handlers
tests/
└── test_tasks.py         ← Pytest suite
requirements.txt          ← Runtime + test deps
```

The `tasks.db` file is correctly identified as a runtime artefact that must be gitignored. The `requirements.txt` dependency list (fastapi, uvicorn, sqlalchemy, httpx, pytest) is complete for the described implementation.

### 4.7 Design Decisions Review

All eight design decisions (DD-01 through DD-08) are reviewed:

| Decision | Rationale Quality | Verdict |
|----------|------------------|---------|
| DD-01 — SQLAlchemy ORM | Cleaner code; avoids SQL injection risk from string formatting | Correct |
| DD-02 — Single tasks.db in project root | Simplest for local-only service; no configuration needed | Correct |
| DD-03 — In-memory SQLite for tests | Test isolation; no disk artefacts | Correct |
| DD-04 — StatusEnum in Pydantic only | Keeps DB schema minimal; API-layer validation sufficient for scope | Correct |
| DD-05 — PATCH for partial update | AC-004 explicitly requires partial update semantics | Correct |
| DD-06 — DELETE returns 204 | Standard REST; AC-005 requires it explicitly | Correct |
| DD-07 — No auth or middleware | A-04, A-07 exclude auth; adds no complexity | Correct |
| DD-08 — /tasks prefix on router | Clean URL; router file avoids prefix duplication | Correct |

---

## 5. Agreed Design Decisions

The following design decisions are confirmed and locked for implementation:

| # | Decision |
|---|----------|
| ADD-01 | Three-layer layout: HTTP (router) → CRUD → Persistence (SQLAlchemy/SQLite). |
| ADD-02 | One router file (`src/routers/tasks.py`) with five endpoints. No additional routers needed. |
| ADD-03 | CRUD functions accept `Session` as first argument; no session management inside CRUD. |
| ADD-04 | `TaskUpdate` uses all-optional fields to support partial update semantics (PATCH). |
| ADD-05 | `StatusEnum` enforced at Pydantic layer only; no CHECK constraint in SQLite. |
| ADD-06 | DELETE returns HTTP 204 with no response body. |
| ADD-07 | Tests override `get_db` with an in-memory SQLite session. One test per acceptance criterion. |
| ADD-08 | `tasks.db` is gitignored; created automatically at runtime by `Base.metadata.create_all`. |
| ADD-09 | `requirements.txt` includes: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `httpx`, `pytest`. |

---

## 6. Identified Gaps and Recommendations

No blocking gaps were found. The following minor notes are recorded for implementation awareness:

| # | Note | Action |
|---|------|--------|
| N-01 | `crud.update_task` must skip fields that are `None` in `TaskUpdate` to satisfy AC-004 partial-update semantics. | Developer must implement field-by-field conditional assignment (or `model_dump(exclude_unset=True)` pattern). |
| N-02 | `crud.delete_task` returns the deleted object or `None`. The router must return `Response(status_code=204)` and not attempt to serialise the return value (FastAPI will serialize `None` as `null`, not an empty body). | Developer must use `from fastapi import Response` and return `Response(status_code=204)` explicitly. |
| N-03 | `tasks.db` must be confirmed absent from the repository before first commit. | Verify `.gitignore` contains `tasks.db` entry before any `git add`. |

None of these notes require changes to `architecture.md`. They are implementation guidance only.

---

## 7. Architecture Changes Required

**None.** The architecture document is complete and correct as written. No changes to `docs/plans/architecture.md` are needed.

---

## 8. Final Review Status

| Item | Status |
|------|--------|
| All 5 FRs covered | PASS |
| All 5 ACs achievable | PASS |
| All 4 NFRs satisfied | PASS |
| Three-layer design appropriate | PASS |
| File structure complete and consistent | PASS |
| No over-engineering | PASS |
| Happy-path focus maintained | PASS |
| Architecture changes required | NONE |

**Overall Status: APPROVED**

The architecture is ready to proceed to implementation planning.

---

*Prepared by: Solution Engineer Agent*
*Date: 2026-11-01*
*JIRA Story: KAN-31*
*Workflow ID: WF-2026-004*
