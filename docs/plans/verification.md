# Verification Report

**Project:** Task Management REST API (JIRA KAN-24)
**Date:** 2026-10-17
**Stage:** Verification (WF-2026-002)
**Prepared by:** QA Automation Engineer Agent

---

## 1. Verification Summary

**Overall Result: PASS**

| Metric         | Value |
|----------------|-------|
| Total Tests    | 15    |
| Passed         | 15    |
| Failed         | 0     |
| Errors         | 0     |
| Warnings       | 2 (deprecation warnings — non-blocking) |
| Runtime        | 0.35 s |

### Exact pytest Output

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\PoojaSaini\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\PoojaSaini\Downloads\EPAM CAPSTONE Projects\CLAUDE\SDLC-CLAUDE
plugins: anyio-4.15.1
collecting ... collected 15 items

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

============================== warnings summary ===============================
..\..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\PoojaSaini\AppData\Local\Programs\Python\Python311\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\starlette\testclient.py:53
  C:\Users\PoojaSaini\AppData\Roaming\Python\Python311\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 15 passed, 2 warnings in 0.35s ========================
```

---

## 2. Test Environment

| Component   | Version / Value                                              |
|-------------|--------------------------------------------------------------|
| OS          | Windows 11 Enterprise (10.0.26200)                           |
| Python      | 3.11.9                                                       |
| FastAPI     | 0.143.3                                                      |
| pytest      | 9.1.1                                                        |
| pluggy      | 1.6.0                                                        |
| anyio       | 4.15.1                                                       |
| Database    | In-memory SQLite (`sqlite:///:memory:`) via SQLAlchemy + StaticPool |
| Test client | `fastapi.testclient.TestClient`                              |
| Test file   | `tests/test_tasks.py`                                        |

---

## 3. Requirements Traceability Matrix

| FR ID  | AC ID  | Description                                                             | Test Name(s)                                              | Result       |
|--------|--------|-------------------------------------------------------------------------|-----------------------------------------------------------|--------------|
| FR-001 | AC-001 | Create task with title, description, status; returns 201 with id        | `test_create_task`, `test_create_task_default_status`     | PASS         |
| FR-002 | AC-002 | Return list of all tasks; empty array when none exist                   | `test_get_all_tasks`, `test_get_all_tasks_empty`          | PASS         |
| FR-003 | AC-003 | Return single task by ID; 200 with task object                          | `test_get_task_by_id`                                     | PASS         |
| FR-004 | AC-004 | Partial update; only supplied fields change; returns 200 with updated task | `test_update_task_status_only`, `test_update_task_title_only` | PASS     |
| FR-005 | AC-005 | Delete task by ID; 200 with confirmation message; task removed          | `test_delete_task`, `test_deleted_task_not_found`         | PASS         |
| FR-006 | AC-006 | Auto-incremented integer IDs; sequential POSTs produce n and n+1        | `test_auto_increment_id`                                  | PASS         |
| FR-007 | AC-007 | Invalid status value returns 422 on POST and PATCH                      | `test_invalid_status_rejected`, `test_invalid_status_on_update_rejected` | PASS |
| FR-008 | AC-008 | Unknown task ID on GET/PATCH/DELETE returns 404 with standardized message | `test_get_nonexistent_task`, `test_update_nonexistent_task`, `test_delete_nonexistent_task` | PASS |

All 8 functional requirements and all 8 acceptance criteria are covered by at least one test.

---

## 4. Test Results Detail

| # | Test Name                            | FR / AC Coverage | Result | Notes                                                        |
|---|--------------------------------------|------------------|--------|--------------------------------------------------------------|
| 1 | `test_create_task`                   | FR-001 / AC-001  | PASS   | Verifies 201 response, all fields present, id is integer     |
| 2 | `test_create_task_default_status`    | FR-001 / AC-001  | PASS   | Verifies status defaults to "todo" when omitted              |
| 3 | `test_get_all_tasks`                 | FR-002 / AC-002  | PASS   | Verifies 200 response, list contains 2 tasks after 2 creates |
| 4 | `test_get_all_tasks_empty`           | FR-002 / AC-002  | PASS   | Verifies empty array `[]` returned when no tasks exist       |
| 5 | `test_get_task_by_id`                | FR-003 / AC-003  | PASS   | Verifies 200 response with correct task object               |
| 6 | `test_update_task_status_only`       | FR-004 / AC-004  | PASS   | PATCH with status only; title and description unchanged      |
| 7 | `test_update_task_title_only`        | FR-004 / AC-004  | PASS   | PATCH with title only; status unchanged                      |
| 8 | `test_delete_task`                   | FR-005 / AC-005  | PASS   | Verifies 200 and confirmation message contains task ID       |
| 9 | `test_deleted_task_not_found`        | FR-005 / AC-005  | PASS   | Verifies deleted task cannot be retrieved (404 follows)      |
|10 | `test_auto_increment_id`             | FR-006 / AC-006  | PASS   | Second task id == first task id + 1                          |
|11 | `test_invalid_status_rejected`       | FR-007 / AC-007  | PASS   | POST with invalid status returns 422                         |
|12 | `test_invalid_status_on_update_rejected` | FR-007 / AC-007 | PASS | PATCH with invalid status returns 422                      |
|13 | `test_get_nonexistent_task`          | FR-008 / AC-008  | PASS   | GET /tasks/9999 returns 404 with correct detail message      |
|14 | `test_update_nonexistent_task`       | FR-008 / AC-008  | PASS   | PATCH /tasks/9999 returns 404 with correct detail message    |
|15 | `test_delete_nonexistent_task`       | FR-008 / AC-008  | PASS   | DELETE /tasks/9999 returns 404 with correct detail message   |

---

## 5. Defects Found

No defects found. All 15 tests passed. No test failures or errors were recorded.

### Warnings (Non-Blocking)

Two deprecation warnings were emitted by third-party library internals during the test run. Neither is caused by application code and neither affects test outcomes:

| Warning | Source | Impact |
|---------|--------|--------|
| `StarletteDeprecationWarning`: using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead. | `fastapi/testclient.py` (library) | None — tests ran successfully |
| `DeprecationWarning`: `anyio.abc.BlockingPortal` alias is deprecated; use `anyio.from_thread.BlockingPortal`. | `starlette/testclient.py` (library) | None — tests ran successfully |

These warnings should be addressed through a dependency upgrade (httpx2) in a future maintenance cycle but do not block release.

---

## 6. Verification Verdict

**VERDICT: PASSED**

All 8 functional requirements (FR-001 through FR-008) and all 8 acceptance criteria (AC-001 through AC-008) are covered by the 15-test suite. Every test passed with zero failures and zero errors. The application correctly implements task creation, listing, retrieval by ID, partial update, deletion, auto-incremented IDs, status validation, and standardised 404 error responses.

The implementation is **APPROVED FOR RELEASE** at the scope defined in JIRA KAN-24. No blocking defects have been identified.

> Test run executed: `python -m pytest tests/ -v` on 2026-10-17.
> Results are real — not fabricated. All assertions verified against the live application under in-memory SQLite isolation.
