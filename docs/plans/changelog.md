# Changelog

## [Unreleased] — KAN-31 Task Management REST API

**Branch**: `feature/KAN-31-task-management-api`
**Workflow**: WF-2026-004
**Date**: 2026-11-01
**Author**: Pooja Saini

---

## Summary

Implements a complete Task Management REST API from scratch on Python 3.11.9 with FastAPI, SQLAlchemy 2.x, Pydantic v2, and SQLite. The implementation covers the full CRUD lifecycle for tasks as defined in JIRA story KAN-31.

---

## What Was Built

### New Application Source Files

| File | Description |
|------|-------------|
| `src/__init__.py` | Python package marker for `src/` |
| `src/routers/__init__.py` | Python package marker for `src/routers/` |
| `src/database.py` | SQLAlchemy engine (`tasks.db`), `SessionLocal` factory, `Base`, and `get_db` FastAPI dependency |
| `src/models.py` | `Task` ORM model mapped to the `tasks` table with `id`, `title`, `description`, `status` columns |
| `src/schemas.py` | Pydantic v2 schemas: `TaskCreate`, `TaskUpdate`, `TaskResponse`, and `StatusEnum` literal type |
| `src/crud.py` | Five database operations: `create_task`, `get_tasks`, `get_task`, `update_task`, `delete_task` |
| `src/routers/tasks.py` | `APIRouter` with all five HTTP endpoints |
| `src/main.py` | FastAPI application entry point; registers tasks router under `/tasks` prefix |
| `tests/test_tasks.py` | Pytest happy-path suite with in-memory SQLite override |
| `requirements.txt` | Runtime and test dependencies |

### REST API Endpoints

| Method | Path | Status Code | Requirement |
|--------|------|-------------|-------------|
| POST | /tasks | 201 Created | FR-001, AC-001 |
| GET | /tasks | 200 OK | FR-002, AC-002 |
| GET | /tasks/{id} | 200 OK | FR-003, AC-003 |
| PATCH | /tasks/{id} | 200 OK | FR-004, AC-004 |
| DELETE | /tasks/{id} | 204 No Content | FR-005, AC-005 |

### Data Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary key, autoincrement |
| title | String(255) | NOT NULL |
| description | String | NOT NULL |
| status | String(20) | NOT NULL, Python-side default `"todo"` |

Allowed status values: `todo`, `in_progress`, `done` — enforced by Pydantic `StatusEnum` literal.

---

## Notable Implementation Decisions

- **PATCH partial update** (`crud.update_task`): uses `model_dump(exclude_unset=True)` to apply only the fields supplied by the caller, satisfying AC-004.
- **DELETE returns no body**: router returns `Response(status_code=204)` explicitly to avoid FastAPI serialising a JSON body, satisfying AC-005.
- **In-memory SQLite for tests**: `get_db` dependency is overridden with `sqlite:///:memory:` so tests are fully isolated and leave no files on disk.
- **SQLite file ignored**: `tasks.db` is excluded from source control via the existing `*.db` glob in `.gitignore`.

---

## Test Results

Command: `python -m pytest tests/test_tasks.py -v`

| Test | Acceptance Criterion | Result |
|------|---------------------|--------|
| `test_create_task` | AC-001 — POST /tasks → 201 + task with id | PASSED |
| `test_list_tasks` | AC-002 — GET /tasks → 200 + array | PASSED |
| `test_get_task` | AC-003 — GET /tasks/{id} → 200 + task | PASSED |
| `test_update_task` | AC-004 — PATCH /tasks/{id} → 200, partial update | PASSED |
| `test_delete_task` | AC-005 — DELETE /tasks/{id} → 204, task removed | PASSED |

**Result: 5 passed, 0 failed, 0 errors** (2 non-blocking third-party deprecation warnings, 1.22s)

---

## Code Review Summary

Reviewed by Code Reviewer Agent on 2026-11-01 (commit `ac99149`).

- Blockers: **0**
- Major: **0**
- Minor: **3** (all low-risk, no impact on correctness)
- Info: **2** (informational only)
- Verdict: **APPROVED**

Minor findings (no action required for this PR):
- CR-001: `status` column uses Python-side `default` instead of `server_default` (no functional impact)
- CR-002: `create_all` runs at import time rather than in a lifespan hook (no functional impact; `tasks.db` gitignored)
- CR-003: `override_get_db` has a redundant `create_all` call (harmless)

---

## Known Limitations

Per requirements Section 9, the following are explicitly out of scope:

- Authentication or authorisation
- Multi-user or concurrent access
- Task filtering, search, or pagination
- Error-path test coverage (404 responses exist but are not tested)
- Containerisation or cloud deployment
- Version-pinned dependencies in `requirements.txt`

---

## SDLC Stages Completed

| Stage | Status | Artifact |
|-------|--------|----------|
| Requirements Analysis | APPROVED (human) | docs/plans/requirements.md |
| Architecture Design | COMPLETED | docs/plans/architecture.md |
| Design Review | APPROVED | docs/plans/design-review.md |
| Implementation Planning | APPROVED (human) | docs/plans/impl-plan.md |
| Development | COMPLETED — 5/5 tests passed | src/ |
| Code Review | APPROVED — 0 blockers, 0 majors | docs/plans/code-review.md |
| Verification | PASSED — 5/5 tests | docs/plans/verification.md |

---

*Prepared by: Deploy-Build-Engineer Agent*
*Date: 2026-11-01*
*JIRA Story: KAN-31*
*Workflow ID: WF-2026-004*
