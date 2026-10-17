# Changelog

## Task Management REST API — v1.0.0

**Date:** 2026-10-17
**JIRA Story:** [KAN-24](https://poojasaini11291.atlassian.net/browse/KAN-24)
**Workflow:** WF-2026-002
**Branch:** claude_demo

---

## Summary of Changes

Implemented a complete Task Management REST API using FastAPI and SQLite. The API exposes five CRUD endpoints for creating, listing, retrieving, updating, and deleting tasks. All 8 functional requirements and 8 acceptance criteria from KAN-24 are satisfied. A pytest test suite of 15 tests was written with 100% pass rate.

---

## Files Added

| File | Description |
|------|-------------|
| `src/__init__.py` | Makes `src/` a Python package so pytest-from-root imports work |
| `src/crud.py` | Data-access layer — CRUD operations against the SQLAlchemy session |
| `src/schemas.py` | Pydantic request/response schemas with `Literal` status validation |
| `src/routers/__init__.py` | Makes `src/routers/` a Python package |
| `src/routers/tasks.py` | FastAPI router — 5 REST endpoints (POST, GET, GET/{id}, PATCH/{id}, DELETE/{id}) |
| `tests/__init__.py` | Makes `tests/` a Python package for pytest-from-root execution |
| `tests/conftest.py` | pytest conftest — in-memory SQLite test fixture (see CR-001 note) |
| `.env.example` | Example environment variable file (no secrets) |

---

## Files Modified

| File | Change Description |
|------|--------------------|
| `src/main.py` | Wired up router, added `Base.metadata.create_all` at startup |
| `src/database.py` | Added `SessionLocal`, `get_db` dependency, `Base`; fixed imports |
| `src/models.py` | Defined `Task` SQLAlchemy model with `id`, `title`, `description`, `status` |
| `tests/test_tasks.py` | Full 15-test pytest suite with in-memory SQLite and dependency override |
| `requirements.txt` | Added FastAPI, SQLAlchemy, uvicorn dependencies |
| `requirements-test.txt` | Added pytest, httpx test dependencies |
| `docs/plans/requirements.md` | Requirements document — WF-2026-002 stage output |
| `docs/plans/architecture.md` | Architecture design — WF-2026-002 stage output |
| `docs/plans/design-review.md` | Design review — WF-2026-002 stage output |
| `docs/plans/impl-plan.md` | Implementation plan — WF-2026-002 stage output |
| `docs/plans/code-review.md` | Code review — WF-2026-002 stage output |
| `docs/plans/verification.md` | Verification report — WF-2026-002 stage output |

---

## Test Evidence

**Framework:** pytest 9.1.1
**Python:** 3.11.9
**Platform:** Windows 11 Enterprise (10.0.26200)
**Database (tests):** In-memory SQLite (`sqlite:///:memory:`) via SQLAlchemy + StaticPool

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\PoojaSaini\Downloads\EPAM CAPSTONE Projects\CLAUDE\SDLC-CLAUDE
collected 15 items

tests/test_tasks.py::test_create_task PASSED                             [  6%]
tests/test_tasks.py::test_create_task_default_status PASSED              [ 13%]
tests/test_tasks.py::test_get_all_tasks PASSED                           [ 20%]
tests/test_tasks.py::test_get_all_tasks_empty PASSED                     [ 26%]
tests/test_tasks.py::test_get_task_by_id PASSED                          [ 33%]
tests/test_tasks.py::test_update_task_status_only PASSED                 [ 40%]
tests/test_tasks.py::test_update_task_title_only PASSED                  [ 46%]
tests/test_tasks.py::test_delete_task PASSED                             [ 53%]
tests/test_tasks.py::test_deleted_task_not_found PASSED                  [ 60%]
tests/test_tasks.py::test_auto_increment_id PASSED                       [ 66%]
tests/test_tasks.py::test_invalid_status_rejected PASSED                 [ 73%]
tests/test_tasks.py::test_invalid_status_on_update_rejected PASSED       [ 80%]
tests/test_tasks.py::test_get_nonexistent_task PASSED                    [ 86%]
tests/test_tasks.py::test_update_nonexistent_task PASSED                 [ 93%]
tests/test_tasks.py::test_delete_nonexistent_task PASSED                 [100%]

======================= 15 passed, 2 warnings in 0.35s ========================
```

**Result: 15/15 PASSED | 0 failed | 0 errors | 2 non-blocking deprecation warnings | 0.35 s**

---

## Known Limitations

The following findings were recorded in the code review (docs/plans/code-review.md). None are blockers for this release.

| ID | Severity | Location | Description |
|----|----------|----------|-------------|
| CR-001 | MAJOR | `tests/conftest.py`, `tests/test_tasks.py:11-29` | Dead `client` fixture in `conftest.py` — the entire test setup is re-implemented at module level in `test_tasks.py`. The conftest fixture is never invoked. No tests are broken, but the duplication creates ambiguity and a latent risk for future test additions. Recommend migrating to idiomatic conftest-based fixtures. |
| CR-002 | MINOR | `src/routers/tasks.py`, `src/main.py:4` | Architecture doc specifies `src/router.py` (flat); implementation uses `src/routers/tasks.py` (subdirectory). Functional deviation only — code is correct. Architecture doc should be updated to match. |
| CR-003 | MINOR | `src/database.py:24-25` | `create_tables()` helper defined but never called. `src/main.py` calls `Base.metadata.create_all` directly. Dead code — recommend removing or consolidating. |
| CR-004 | MINOR | `tests/test_tasks.py:28-29` | Dependency override and `TestClient` set at module scope (import time), not inside a pytest fixture. Order-dependent if future test modules also modify `app.dependency_overrides`. Resolved naturally by fixing CR-001. |
| CR-005 | MINOR | `src/tasks.db` | A `tasks.db` file exists inside `src/`. This indicates the app was run from inside `src/` at some point. The `*.db` pattern is in `.gitignore` so the file is not versioned. Confirm `uvicorn src.main:app` is always launched from the project root. |

---

## Requirements Traceability

All 8 functional requirements (FR-001 through FR-008) and all 8 acceptance criteria (AC-001 through AC-008) from JIRA KAN-24 are satisfied. See `docs/plans/verification.md` for full traceability matrix.

---

## Approval Chain

| Stage | Status | Date |
|-------|--------|------|
| Requirements Analysis | APPROVED (human) | 2026-10-17 |
| Architecture Design | COMPLETED | 2026-10-17 |
| Design Review | COMPLETED | 2026-10-17 |
| Implementation Planning | APPROVED (human) | 2026-10-17 |
| Development | COMPLETED | 2026-10-17 |
| Code Review | PASS WITH NOTES | 2026-10-17 |
| Verification | PASSED (15/15) | 2026-10-17 |
| Release / PR | PENDING HUMAN APPROVAL | 2026-10-17 |
