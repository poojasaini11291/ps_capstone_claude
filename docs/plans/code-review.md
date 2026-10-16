
# Code Review
## Task Management REST API

**Workflow ID:** WF-2026-001
**Stage:** Code Review
**Author:** Code Reviewer Agent
**Date:** 2026-10-17
**Branch:** feature/task-management-api
**Inputs:** docs/plans/requirements.md, docs/plans/architecture.md, src/

---

## 1. Review Summary

The implementation is clean, readable, and correctly structured. All 8 functional requirements are satisfied. The code aligns with the approved architecture. No blockers or major issues were found. Three minor findings are recorded — none require rework before testing.

**Verdict: PASS — proceed to verification.**

---

## 2. Requirements Compliance

| Req ID | Requirement | File | Status |
|--------|-------------|------|--------|
| FR-001 | Create task | `routers/tasks.py:12-22` | ✅ POST `/tasks/` with `TaskCreate` validation; returns 201 + task object |
| FR-002 | View all tasks | `routers/tasks.py:25-27` | ✅ GET `/tasks/` returns full list |
| FR-003 | View by ID | `routers/tasks.py:30-38` | ✅ GET `/tasks/{task_id}` with 404 on miss |
| FR-004 | Partial update | `routers/tasks.py:41-54` | ✅ PATCH with `model_dump(exclude_none=True)` updates only supplied fields |
| FR-005 | Delete task | `routers/tasks.py:57-67` | ✅ DELETE with 404 on miss, returns confirmation message |
| FR-006 | Auto-increment ID | `models.py:8` | ✅ `autoincrement=True`, `primary_key=True` |
| FR-007 | Status enum | `schemas.py:8,14` | ✅ `Literal["todo","in_progress","done"]` in both `TaskCreate` and `TaskUpdate` |
| FR-008 | 404 with message | `routers/tasks.py:34-37,44-48,61-64` | ✅ `"Task with ID {id} does not exist"` in all three endpoints |

**Compliance: 8 / 8 — complete.**

---

## 3. Architecture Alignment

| Architecture Item | Expected | Actual | Status |
|-------------------|----------|--------|--------|
| File structure | `src/main.py`, `database.py`, `models.py`, `schemas.py`, `routers/tasks.py` | All present | ✅ |
| DB session pattern | `get_db()` generator with `Depends` | `database.py:13-18` | ✅ |
| Pydantic v2 config | `ConfigDict(from_attributes=True)` | `schemas.py:18` | ✅ |
| PATCH partial update | `model_dump(exclude_none=True)` | `routers/tasks.py:49` | ✅ |
| Router prefix | `/tasks` | `main.py:9` | ✅ |
| Table creation | `create_tables()` on startup | `main.py:5` | ✅ |

---

## 4. Findings

### F-001 — `declarative_base()` deprecated in SQLAlchemy 2.x (MINOR)

**File:** `src/database.py:10`
**Code:** `Base = declarative_base()`
**Issue:** In SQLAlchemy 2.0+, `declarative_base()` is a legacy API that emits a `MovedIn20Warning`. The modern approach is:
```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```
**Impact:** Deprecation warning in logs; no functional impact on SQLAlchemy 2.1.4.
**Recommendation:** Update before future SQLAlchemy upgrades remove the legacy API.
**Severity:** MINOR — does not block testing or functionality.

---

### F-002 — 404 fetch pattern duplicated across 3 endpoints (MINOR)

**Files:** `src/routers/tasks.py:32-37`, `43-48`, `59-64`
**Issue:** The "fetch task by id, raise 404 if not found" pattern appears identically in `get_task`, `update_task`, and `delete_task`. This is a refactor candidate:
```python
def get_task_or_404(task_id: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail=f"Task with ID {task_id} does not exist")
    return task
```
**Impact:** None — the duplication is 3 occurrences and fully readable as-is.
**Recommendation:** Optional refactor; acceptable for current scope.
**Severity:** MINOR — no functional issue.

---

### F-003 — `create_tables()` called at module import time (MINOR)

**File:** `src/main.py:5`
**Code:** `create_tables()` called at module level before `app` is defined.
**Issue:** Any test that imports `main` will trigger `create_tables()`, which creates `tasks.db` in the current working directory. For happy-path tests using a real DB this is acceptable, but the test runner must be launched from `src/` to resolve the relative path `./tasks.db` correctly.
**Impact:** Tests will fail with a path error if run from the project root without `cd src/` first.
**Recommendation:** Automation tester must run pytest from `src/` or configure `pythonpath` in `pytest.ini`. No code change required.
**Severity:** MINOR — test execution note, not a code defect.

---

## 5. Security Review

| Check | Result |
|-------|--------|
| SQL injection | ✅ ORM used throughout — no raw SQL |
| Input validation | ✅ Pydantic validates all inputs at request time |
| Status enum enforcement | ✅ `Literal` type rejects invalid values with 422 |
| Secrets in code | ✅ None — only `sqlite:///./tasks.db` (local path, not a secret) |
| Authentication | N/A — intentionally out of scope per requirements |

---

## 6. Readability

| Criterion | Assessment |
|-----------|------------|
| Naming | Clear: `create_task`, `get_tasks`, `get_task`, `update_task`, `delete_task` |
| Function length | All functions ≤ 12 lines |
| Module size | All files ≤ 25 lines |
| No unnecessary comments | ✅ Code is self-documenting |
| No dead code | ✅ Every import and function is used |

---

## 7. Blocking Findings

**None.** All findings are MINOR. No developer rework required before proceeding to verification.

---

## 8. Final Verdict

**PASS — no blockers. Proceed to Stage 7: Verification.**
