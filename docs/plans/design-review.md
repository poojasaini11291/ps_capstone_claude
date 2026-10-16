
# Design Review
## Task Management REST API

**Workflow ID:** WF-2026-001
**Stage:** Design Review
**Author:** Solution Engineer Agent
**Date:** 2026-10-17
**Inputs:** docs/plans/requirements.md, docs/plans/architecture.md

---

## 1. Review Summary

The architecture is well-suited to the requirements. It is simple, correctly scoped, and avoids over-engineering. All 8 functional requirements and 4 non-functional requirements have direct architecture coverage. Three minor observations are recorded below — none require architecture changes; one warrants a developer note.

**Overall verdict: APPROVED WITH NOTES**

---

## 2. Requirements Coverage

| Req ID | Requirement | Architecture Coverage | Status |
|--------|--------------|-----------------------|--------|
| FR-001 | Create task | `POST /tasks` → `TaskCreate` schema → router writes to SQLite | ✅ Covered |
| FR-002 | View all tasks | `GET /tasks` → query all rows → list of `TaskResponse` | ✅ Covered |
| FR-003 | View by ID | `GET /tasks/{id}` → query by id → `TaskResponse` | ✅ Covered |
| FR-004 | Partial update | `PATCH /tasks/{id}` → `TaskUpdate` (all fields optional) → update only provided fields | ✅ Covered |
| FR-005 | Delete | `DELETE /tasks/{id}` → delete row → confirmation message | ✅ Covered |
| FR-006 | Auto-increment ID | SQLite `AUTOINCREMENT` on `id` column | ✅ Covered |
| FR-007 | Status restricted to enum | Pydantic `Literal["todo", "in_progress", "done"]` in both create and update schemas | ✅ Covered |
| FR-008 | 404 with message | Router raises `HTTPException(404)` with `"Task with ID {id} does not exist"` | ✅ Covered |
| NFR-001 | Python + FastAPI | FastAPI application | ✅ Covered |
| NFR-002 | SQLite persistence | SQLAlchemy + SQLite `tasks.db` | ✅ Covered |
| NFR-003 | JSON responses | FastAPI returns JSON by default; `TaskResponse` Pydantic model serializes to JSON | ✅ Covered |
| NFR-004 | Local, no infra | Single process, local SQLite file | ✅ Covered |

**Coverage: 12 / 12 — complete.**

---

## 3. Findings

### Finding 1 — Pydantic version alignment (MINOR)
**Observation:** The architecture uses `class Config: from_attributes = True` inside `TaskResponse`. This is the Pydantic v2 syntax. If `requirements.txt` pins `pydantic<2`, the correct syntax is `orm_mode = True` under `class Config`. Mixing versions causes a silent misconfiguration.

**Recommendation:** Pin `pydantic>=2.0` in `requirements.txt`, or explicitly note the version assumption in the developer handoff. No architecture change needed.

---

### Finding 2 — DB session lifecycle (MINOR, developer note)
**Observation:** `database.py` is listed as responsible for "session factory." FastAPI's standard pattern uses a `get_db()` dependency injected into each route via `Depends(get_db)`. The architecture diagram does not make this explicit, which could lead to session-per-app (not per-request) implementations that leave connections open.

**Recommendation:** Developer must implement the `get_db` generator pattern:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
No architecture document change needed — this is an implementation detail for the developer.

---

### Finding 3 — `httpx` test dependency scope (MINOR)
**Observation:** `httpx` is listed in `requirements.txt` (production deps) but is only needed for testing (`httpx` is required by FastAPI's `TestClient`). For a local project this is harmless, but conventionally test-only deps belong in a separate `requirements-test.txt` or `requirements-dev.txt`.

**Recommendation:** Developer may place `httpx` and `pytest` in a `requirements-test.txt`. No blocker — either approach works for this scope.

---

## 4. Agreed Design Decisions

| Decision | Agreed Value | Source |
|----------|-------------|--------|
| Status values | `todo`, `in_progress`, `done` | User clarification Q1 |
| Description on create | Required | User clarification Q2 |
| Update method | PATCH (partial) | User clarification Q3 |
| ID type | Auto-incremented integer | User clarification Q4 |
| List endpoint | Flat list, no filters | User clarification Q5 |
| Not-found response | 404 + `"Task with ID {id} does not exist"` | User clarification Q6 |
| Default status | `todo` | Architecture decision |
| ORM | SQLAlchemy | Architecture decision |
| No auth | Intentional out-of-scope | Requirements |

---

## 5. Architecture Changes Required

**None.** The architecture document does not need modification. Findings 1–3 are implementation-level notes for the developer.

---

## 6. Final Review Status

**APPROVED — proceed to Stage 4: Implementation Planning.**
