# Pull Request Draft

**Branch**: `feature/KAN-31-task-management-api` → `main`
**JIRA Story**: [KAN-31](https://poojasaini11291.atlassian.net/browse/KAN-31)
**Workflow**: WF-2026-004
**Status**: AWAITING HUMAN APPROVAL BEFORE CREATION

---

## PR Title

`feat(KAN-31): implement Task Management REST API`

---

## Summary

Implements a complete Task Management REST API for JIRA story KAN-31. The service exposes five CRUD endpoints backed by SQLite (via SQLAlchemy), with Pydantic v2 request/response validation. The implementation covers every acceptance criterion from the approved requirements and passes all 5 happy-path tests.

All SDLC stages have been completed: requirements (human-approved), architecture, design review, implementation planning (human-approved), development, code review (0 blockers), and verification (5/5 tests passed).

---

## Changes Made

### New Source Files

| File | Description |
|------|-------------|
| `src/__init__.py` | Package marker |
| `src/routers/__init__.py` | Package marker for routers sub-package |
| `src/database.py` | SQLAlchemy engine, `SessionLocal`, `Base`, `get_db` dependency |
| `src/models.py` | `Task` ORM model (`id`, `title`, `description`, `status`) |
| `src/schemas.py` | Pydantic v2: `TaskCreate`, `TaskUpdate`, `TaskResponse`, `StatusEnum` |
| `src/crud.py` | `create_task`, `get_tasks`, `get_task`, `update_task`, `delete_task` |
| `src/routers/tasks.py` | `APIRouter` — five HTTP endpoints under `/tasks` |
| `src/main.py` | FastAPI app entry point; registers router; creates DB tables on startup |
| `tests/test_tasks.py` | Pytest happy-path suite (in-memory SQLite override) |
| `requirements.txt` | `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `httpx`, `pytest` |

### REST API Endpoints Implemented

| Method | Path | Response | Requirement |
|--------|------|----------|-------------|
| POST | /tasks | 201 + task object | FR-001 |
| GET | /tasks | 200 + task array | FR-002 |
| GET | /tasks/{id} | 200 + task object | FR-003 |
| PATCH | /tasks/{id} | 200 + updated task | FR-004 |
| DELETE | /tasks/{id} | 204 No Content | FR-005 |

### Key Implementation Details

- **PATCH partial update**: `crud.update_task` uses `model_dump(exclude_unset=True)` so only supplied fields are written (satisfies AC-004).
- **DELETE 204**: endpoint returns `Response(status_code=204)` explicitly — no serialised body (satisfies AC-005, design review note N-02).
- **Status validation**: `StatusEnum = Literal["todo", "in_progress", "done"]` enforced at the Pydantic layer (satisfies A-02).
- **Test isolation**: `get_db` overridden with `sqlite:///:memory:` in tests; `reset_db` autouse fixture drops and recreates tables before each test.

---

## Test Evidence

**Command**: `python -m pytest tests/test_tasks.py -v`
**Environment**: Python 3.11.9, pytest 9.1.1, Windows 11

```
tests/test_tasks.py::test_create_task PASSED    [ 20%]
tests/test_tasks.py::test_list_tasks  PASSED    [ 40%]
tests/test_tasks.py::test_get_task    PASSED    [ 60%]
tests/test_tasks.py::test_update_task PASSED    [ 80%]
tests/test_tasks.py::test_delete_task PASSED    [100%]

======================== 5 passed, 2 warnings in 1.22s ========================
```

2 deprecation warnings from third-party libraries (`httpx`/`starlette`) — non-blocking; no warnings from application code.

| Test | Acceptance Criterion | Result |
|------|---------------------|--------|
| `test_create_task` | AC-001 | PASSED |
| `test_list_tasks` | AC-002 | PASSED |
| `test_get_task` | AC-003 | PASSED |
| `test_update_task` | AC-004 | PASSED |
| `test_delete_task` | AC-005 | PASSED |

---

## Code Review Summary

Reviewed at commit `ac99149`:

- **Blockers**: 0
- **Major**: 0
- **Minor**: 3 (low-risk, no correctness impact)
- **Info**: 2
- **Verdict**: APPROVED

Minor findings (no PR blocking):
- CR-001: `status` column uses Python-side `default` instead of `server_default` (no functional impact)
- CR-002: `Base.metadata.create_all` called at import time (no security/correctness impact; `tasks.db` is gitignored)
- CR-003: Redundant `create_all` in test override (harmless)

---

## SDLC Stages Completed

| Stage | Status | Date |
|-------|--------|------|
| Requirements Analysis | APPROVED (human) | 2026-11-01 |
| Architecture Design | COMPLETED | 2026-11-01 |
| Design Review | APPROVED | 2026-11-01 |
| Implementation Planning | APPROVED (human) | 2026-11-01 |
| Development | COMPLETED — 5/5 tests passed | 2026-11-01 |
| Code Review | APPROVED — 0 blockers, 0 majors | 2026-11-01 |
| Verification | PASSED — 5/5 tests | 2026-11-01 |

---

## Known Limitations

Explicitly out of scope per requirements (Section 9):

- No authentication or authorisation
- No multi-user or concurrent access support
- No task filtering, search, or pagination
- Error-path test coverage (404 paths exist but are not tested)
- No containerisation or cloud deployment
- No pinned dependency versions in `requirements.txt`

---

## Reviewer Checklist

- [ ] All 5 endpoints exist and return the correct HTTP status codes
- [ ] PATCH partial update only modifies supplied fields (AC-004)
- [ ] DELETE returns 204 with empty body (AC-005)
- [ ] `tasks.db` is not committed (covered by `*.db` in `.gitignore`)
- [ ] No secrets or credentials in source code
- [ ] All 5 tests pass locally (`python -m pytest tests/test_tasks.py -v`)
- [ ] Requirements traceability: all FRs and ACs covered
- [ ] SDLC artifacts present under `docs/plans/`

---

*Prepared by: Deploy-Build-Engineer Agent*
*Date: 2026-11-01*
*JIRA Story: KAN-31*
*Workflow ID: WF-2026-004*

🤖 Generated with [Claude Code](https://claude.com/claude-code)
