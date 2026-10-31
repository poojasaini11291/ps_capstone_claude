# Requirements Document

## 1. JIRA Story Details

- **JIRA Story Key**: KAN-31
- **JIRA Story URL**: https://poojasaini11291.atlassian.net/browse/KAN-31
- **Summary**: Task Management REST API — Requirements 1
- **Priority**: Medium
- **Status**: To Do
- **Reporter**: Pooja Saini
- **Assignee**: Pooja Saini

---

## 2. Project Objective

Build a simple Task Management REST API that allows users to create, view, update, and delete tasks. The API must persist tasks in SQLite and expose a clean REST interface via FastAPI. The goal is a locally-runnable, dependency-light service that covers the full CRUD lifecycle for tasks.

---

## 3. Original User Story

> As a user, I want to create, view, update and delete tasks, so that I can manage my daily activities.

---

## 4. Functional Requirements

| ID     | Requirement |
|--------|-------------|
| FR-001 | The system shall allow a user to create a task with title, description, and status. |
| FR-002 | The system shall return a list of all tasks. |
| FR-003 | The system shall return a single task by its ID. |
| FR-004 | The system shall allow a user to partially update a task (title, description, or status). |
| FR-005 | The system shall allow a user to delete a task by its ID. |

**Note on FR-005**: The JIRA story body lists DELETE /tasks/{id} as an API endpoint and the user story explicitly names "delete tasks" as a needed operation. JIRA omitted a formal requirement ID and acceptance criteria row for this endpoint. FR-005 has been added to close that gap; see Section 11 (Clarification Summary) for the decision rationale.

### Data Model

| Field       | Type    | Required | Notes |
|-------------|---------|----------|-------|
| id          | integer | system   | Auto-incremented; assigned on create |
| title       | string  | yes      | Provided by user |
| description | string  | yes      | Provided by user |
| status      | string  | yes      | Allowed values: `todo`, `in_progress`, `done`. Default: `todo` |

---

## 5. Non-Functional Requirements

| ID      | Requirement |
|---------|-------------|
| NFR-001 | The API must be implemented in Python using FastAPI. |
| NFR-002 | Task data must persist using SQLite (no external database). |
| NFR-003 | All API responses must use JSON format. |
| NFR-004 | The application must run locally without external infrastructure. |

---

## 6. Acceptance Criteria

| ID     | Given / When / Then |
|--------|---------------------|
| AC-001 | **Given** a valid request body with title, description, and optional status, **when** POST /tasks is called, **then** the API returns HTTP 201 Created with the created task object including its assigned `id`. |
| AC-002 | **Given** the task store (empty or populated), **when** GET /tasks is called, **then** the API returns HTTP 200 OK with a JSON array of all tasks (empty array `[]` when no tasks exist). |
| AC-003 | **Given** a task with the requested `id` exists, **when** GET /tasks/{id} is called, **then** the API returns HTTP 200 OK with the matching task object. |
| AC-004 | **Given** a task with the requested `id` exists, **when** PATCH /tasks/{id} is called with one or more fields (title, description, status), **then** the API returns HTTP 200 OK; only the supplied fields are updated and the remaining fields retain their previous values. |
| AC-005 | **Given** a task with the requested `id` exists, **when** DELETE /tasks/{id} is called, **then** the API returns HTTP 204 No Content and the task is removed from the store. |

---

## 7. Assumptions

| # | Assumption |
|---|------------|
| A-01 | FR-005 (DELETE) is intentionally scoped in. The user story's phrase "delete tasks" and the presence of DELETE /tasks/{id} in the API Endpoints table confirm the intent; the missing requirement ID and acceptance criteria row in JIRA were an oversight. |
| A-02 | The `status` field accepts exactly three values: `todo`, `in_progress`, `done`. Any other value is invalid. |
| A-03 | `title` and `description` are required at task creation; partial update via PATCH allows either field to be omitted. |
| A-04 | There is no authentication or authorisation — the API is open to any local caller. |
| A-05 | The SQLite database file will be stored locally alongside the application code. |
| A-06 | The application runs on localhost; no production or cloud deployment is needed. |
| A-07 | A single-user, single-instance deployment is sufficient (no concurrency guarantees required). |

---

## 8. Dependencies

| # | Dependency |
|---|------------|
| D-01 | Python 3.10+ runtime |
| D-02 | FastAPI web framework |
| D-03 | SQLite (bundled with Python standard library) |
| D-04 | Pytest for automated testing |
| D-05 | A SQLite ORM or direct sqlite3 driver for persistence |

---

## 9. Out of Scope

The following are explicitly excluded from this implementation:

- Authentication and authorisation
- Multi-user support
- Task filtering, search, or pagination
- Task priorities, due dates, tags, or attachments
- Notifications or email
- Cloud deployment or containerisation
- Error handling beyond happy-path scenarios (e.g., 404 for non-existent task ID is noted but test coverage focuses on happy paths)

---

## 10. Requirements Traceability

| JIRA Story | Requirement ID | Acceptance Criteria | Description |
|------------|----------------|---------------------|-------------|
| KAN-31     | FR-001         | AC-001              | Create a task via POST /tasks |
| KAN-31     | FR-002         | AC-002              | Retrieve all tasks via GET /tasks |
| KAN-31     | FR-003         | AC-003              | Retrieve a single task via GET /tasks/{id} |
| KAN-31     | FR-004         | AC-004              | Partially update a task via PATCH /tasks/{id} |
| KAN-31     | FR-005         | AC-005              | Delete a task via DELETE /tasks/{id} (gap-filled) |

---

## 11. Clarification Summary

### Gap Identified

**Q1**: The JIRA story's user story explicitly states "delete tasks" and lists `DELETE /tasks/{id}` in the API Endpoints table, but there is no corresponding functional requirement (FR-005) or acceptance criteria row for the delete operation. Should DELETE be treated as in scope?

**Decision**: Yes — the evidence within the JIRA story itself (user story wording + API endpoint listing) is unambiguous. The missing requirement row is an oversight in the JIRA entry, not an intentional exclusion. FR-005 and AC-005 have been added to close the gap. This decision has been documented as Assumption A-01 and is subject to human reviewer confirmation at the approval checkpoint below.

### Decisions Made

| # | Decision |
|---|----------|
| DC-01 | DELETE /tasks/{id} is included as FR-005 with AC-005 (HTTP 204 No Content on success). |
| DC-02 | Happy-path focus retained; error-path testing (e.g., 404) is noted in out-of-scope but the endpoint itself must exist. |
| DC-03 | All four status values (`todo`, `in_progress`, `done`) and the default value (`todo`) are preserved from JIRA's data model. |

---

## 12. Approval Status

**Status**: APPROVED

Approved by: Human (explicit confirmation received 2026-11-01)

Prepared by: Business Analyst Agent
Date: 2026-11-01
JIRA Story: KAN-31
