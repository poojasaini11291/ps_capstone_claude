# Design Review

**JIRA Story:** KAN-24 — Task Management REST API
**Review Date:** 2026-10-17
**Reviewer Role:** Senior Solution Engineer
**Input Artifacts:**
- `docs/plans/requirements.md` (approved 2026-10-17)
- `docs/plans/architecture.md`

---

## 1. Review Summary

The architecture is sound, minimal, and directly traceable to every requirement in KAN-24. All eight functional requirements and all four non-functional requirements are fully addressed. The layered module design (router → crud → models → database) enforces single responsibility and is the correct minimal structure for a local FastAPI + SQLAlchemy + SQLite CRUD API. One minor documentation gap was identified: the architecture did not explicitly state that FastAPI's `HTTPException` wraps the FR-008 error message in a `{"detail": "..."}` JSON envelope, which could cause ambiguity during implementation. This gap has been corrected in `architecture.md` (see Section 5). No structural, API, or data-model deficiencies were found.

**Verdict: APPROVED WITH CHANGES** — one minor clarification applied to `architecture.md`.

---

## 2. Requirements Coverage

### Functional Requirements

| ID     | Requirement Summary | Satisfying Component(s) | Coverage |
|--------|---------------------|-------------------------|----------|
| FR-001 | Create task with title, description, status | `POST /tasks` route in `router.py`; `TaskCreate` schema in `schemas.py`; `create_task` in `crud.py` | COVERED |
| FR-002 | Return list of all tasks | `GET /tasks` route in `router.py`; `get_tasks` in `crud.py` | COVERED |
| FR-003 | Return single task by ID | `GET /tasks/{id}` route in `router.py`; `get_task` in `crud.py` | COVERED |
| FR-004 | Partially update a task | `PATCH /tasks/{id}` route in `router.py`; `TaskUpdate` (all-optional schema) in `schemas.py`; `update_task` with `model_dump(exclude_unset=True)` in `crud.py` | COVERED |
| FR-005 | Delete task by ID | `DELETE /tasks/{id}` route in `router.py`; `delete_task` in `crud.py` | COVERED |
| FR-006 | Auto-incremented integer ID | `id` column defined as `Integer, Primary Key, autoincrement=True` in `models.py`; excluded from `TaskCreate` and `TaskUpdate` schemas | COVERED |
| FR-007 | Status restricted to todo/in_progress/done; default todo | `Literal["todo", "in_progress", "done"]` in `TaskCreate` and `TaskUpdate` schemas; `default="todo"` in ORM model and `TaskCreate` schema | COVERED |
| FR-008 | 404 with message "Task with ID {id} does not exist" for unknown IDs | `HTTPException(404, "Task with ID {id} does not exist")` raised by route handlers for GET/{id}, PATCH/{id}, DELETE/{id} | COVERED |

### Non-Functional Requirements

| ID      | Requirement Summary | Satisfying Component(s) | Coverage |
|---------|---------------------|-------------------------|----------|
| NFR-001 | Python + FastAPI | Technology stack: Python 3.11+, FastAPI 0.110+ | COVERED |
| NFR-002 | SQLite persistence, no external DB server | `database.py` configures SQLAlchemy with SQLite file; no external service required | COVERED |
| NFR-003 | JSON responses | FastAPI serializes all responses via Pydantic (`TaskResponse`, delete confirmation dict); JSON is the default wire format | COVERED |
| NFR-004 | Run locally with no external infrastructure | All components in one process; SQLite embedded; Uvicorn local ASGI server; no cloud or message broker dependency | COVERED |

**Coverage summary: 8/8 FRs COVERED, 4/4 NFRs COVERED.**

---

## 3. Findings

### DR-001

- **ID:** DR-001
- **Severity:** MINOR
- **Description:** The architecture's Section 4 Notes stated that 404 responses use the message `"Task with ID {id} does not exist"` but did not specify the JSON envelope. FastAPI's `HTTPException` serialises errors as `{"detail": "<message>"}`. Without this explicit statement, an implementer could return a bare string or a differently keyed object, which would pass the requirements' message-text check but produce a non-standard response shape.
- **Recommendation:** Document the exact JSON envelope format for 404 responses. **Applied:** Section 4 Notes updated to: `{"detail": "Task with ID {id} does not exist"}`. No structural change to the architecture.

---

### DR-002

- **ID:** DR-002
- **Severity:** INFO
- **Description:** The `TaskResponse` Pydantic schema defines `status` as plain `str` rather than `Literal["todo", "in_progress", "done"]`. Because task status values are only ever written through `TaskCreate` and `TaskUpdate` (which do constrain the field with `Literal`), there is zero runtime risk of an invalid status appearing in a response. However, using `str` makes the response schema less self-documenting in the generated OpenAPI specification.
- **Recommendation:** Tightening `TaskResponse.status` to `Literal["todo", "in_progress", "done"]` would improve OpenAPI clarity at no cost. This is not required for correctness and may be deferred to the implementation phase.

---

### DR-003

- **ID:** DR-003
- **Severity:** INFO
- **Description:** Section 9 states the database is stored as "a local file (`tasks.db` at the project root or configurable via an environment variable)" but does not name the environment variable or provide the exact default path. This leaves the implementer to decide, which could cause inconsistency between the application and the test fixtures.
- **Recommendation:** Specify the default path as `./tasks.db` relative to the working directory (i.e., the project root when started with `uvicorn src.main:app`), and name the environment variable (e.g., `DATABASE_URL`) if runtime overriding is desired. No architecture change is required; this can be resolved at the implementation stage with a comment in `database.py`.

---

### DR-004

- **ID:** DR-004
- **Severity:** INFO
- **Description:** Pydantic v2 requires `model_config = ConfigDict(from_attributes=True)` on `TaskResponse` to serialise SQLAlchemy ORM objects. This is referenced in Section 9 ("Pydantic's `from_attributes` mode") but is not shown in the schema definitions in Section 5. An implementer reading only Section 5 would not know this configuration is required and could encounter a runtime `ValidationError`.
- **Recommendation:** Add a brief note to the `TaskResponse` definition in Section 5 stating that `model_config = ConfigDict(from_attributes=True)` is required. This is an implementation reminder, not a structural gap; it may be addressed at the implementation stage.

---

## 4. Agreed Design Decisions

The following design decisions from the architecture are confirmed as correct for the given scope:

| Decision | Rationale | Confirmed |
|----------|-----------|-----------|
| FastAPI over Flask | Built-in Pydantic validation delivers FR-007/AC-007 (422 on invalid status) as zero-cost built-in behavior, and generates OpenAPI docs automatically. | Yes |
| SQLAlchemy ORM over raw sqlite3 | ORM model serves as schema source of truth; `Base.metadata.create_all` removes manual DDL; Pydantic `from_attributes` serialisation avoids manual row mapping. | Yes |
| Synchronous SQLAlchemy (no AsyncSession) | SQLite is file-locked; async I/O yields no benefit. Synchronous code is simpler and correct for a single-user local API. | Yes |
| Separate `crud.py` from `router.py` | Thin route handlers and isolated data-access functions; CRUD functions are independently testable without an HTTP layer. | Yes |
| Pydantic schemas separate from ORM models | Decouples API contract from database schema; `id` exclusion from `TaskCreate`/`TaskUpdate` is automatic with no extra code, satisfying FR-006/A-05. | Yes |
| In-memory SQLite for tests | Test isolation with no side-effects on the development database file; no teardown required beyond session scope. | Yes |
| PATCH uses `model_dump(exclude_unset=True)` | Correct implementation of partial update semantics (FR-004/AC-004): only explicitly supplied fields are updated; absent fields remain unchanged. | Yes |

---

## 5. Architecture Changes Required

One change was applied to `docs/plans/architecture.md`:

| Change | Location | Before | After |
|--------|----------|--------|-------|
| Clarify 404 response JSON envelope format | Section 4 — REST API Endpoint Design, Notes, bullet 3 | `404 responses use the standardized message: "Task with ID {id} does not exist" (FR-008).` | `404 responses use FastAPI's standard HTTPException JSON envelope: {"detail": "Task with ID {id} does not exist"} (FR-008). The detail key is FastAPI's built-in error wrapper; the message text matches FR-008 exactly.` |

This is a documentation clarification only. No module responsibilities, endpoint definitions, data model, or data-flow steps were altered.

---

## 6. Final Review Status

**APPROVED WITH MINOR NOTES**

The architecture fully satisfies all functional and non-functional requirements from KAN-24. The single architecture update (DR-001) has been applied and is a documentation clarification, not a structural correction. Findings DR-002, DR-003, and DR-004 are informational and are addressed at the implementation stage with no architecture re-work required. The implementation planning stage may proceed.
