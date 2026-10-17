# Requirements Document

## 1. JIRA Story Details

- **JIRA Story Key:** KAN-24
- **JIRA Story URL:** https://poojasaini11291.atlassian.net/browse/KAN-24
- **Summary:** Task Management REST API — Requirements
- **Project:** PS EPAM Capstone (KAN)
- **Issue Type:** Story
- **Priority:** Medium
- **Status:** To Do
- **Reporter:** Pooja Saini

---

## 2. Project Objective

Build a simple Task Management REST API that enables users to create, view, update, and delete tasks. The API must persist tasks in a SQLite database and expose a clean REST interface implemented with FastAPI. The application must run locally with no external infrastructure dependencies.

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
| FR-006 | Each task shall have an auto-incremented integer ID assigned by the system on creation. |
| FR-007 | Task status shall be restricted to the values: `todo`, `in_progress`, `done`. Default value is `todo`. |
| FR-008 | When a task ID does not exist, the system shall return HTTP 404 with the message: `"Task with ID {id} does not exist"`. |

---

## 5. Data Model

| Field       | Type    | Required       | Notes                                              |
|-------------|---------|----------------|----------------------------------------------------|
| id          | integer | system-assigned | Auto-incremented; assigned on create, not by user |
| title       | string  | yes            | Provided by the user                               |
| description | string  | yes            | Provided by the user                               |
| status      | string  | yes            | One of: `todo`, `in_progress`, `done`. Default: `todo` |

---

## 6. API Endpoints

| Method | Path          | Description                    |
|--------|---------------|--------------------------------|
| POST   | /tasks        | Create a new task              |
| GET    | /tasks        | Retrieve all tasks             |
| GET    | /tasks/{id}   | Retrieve a task by ID          |
| PATCH  | /tasks/{id}   | Partially update a task        |
| DELETE | /tasks/{id}   | Delete a task by ID            |

---

## 7. Non-Functional Requirements

| ID      | Requirement |
|---------|-------------|
| NFR-001 | The application shall be implemented in Python using the FastAPI framework. |
| NFR-002 | Tasks shall be persisted using SQLite (no external database server required). |
| NFR-003 | All API responses shall use JSON format. |
| NFR-004 | The application shall run locally with no external infrastructure dependencies. |

---

## 8. Acceptance Criteria

**AC-001** — Mapped to FR-001 (Create Task)

- Given a POST request to `/tasks` with valid `title`, `description`, and optional `status` fields
- When the request is processed
- Then the system returns HTTP 201 Created with a JSON task object that includes the system-assigned `id`

---

**AC-002** — Mapped to FR-002 (List All Tasks)

- Given a GET request to `/tasks`
- When the request is processed
- Then the system returns HTTP 200 OK with a JSON array of all tasks
- And if no tasks exist, an empty JSON array `[]` is returned

---

**AC-003** — Mapped to FR-003 (Get Task by ID)

- Given a GET request to `/tasks/{id}` with a valid existing task ID
- When the request is processed
- Then the system returns HTTP 200 OK with the JSON task object for that ID

---

**AC-004** — Mapped to FR-004 (Partial Update)

- Given a PATCH request to `/tasks/{id}` with one or more of the fields `title`, `description`, or `status`
- When the request is processed
- Then the system returns HTTP 200 OK with the updated task object
- And only the supplied fields are updated; all other fields remain unchanged

---

**AC-005** — Mapped to FR-005 (Delete Task)

- Given a DELETE request to `/tasks/{id}` with a valid existing task ID
- When the request is processed
- Then the system returns HTTP 200 OK with a JSON confirmation message
- And the task is removed from the database

---

**AC-006** — Mapped to FR-006 (Auto-Incremented ID)

- Given two sequential POST requests to `/tasks`
- When both requests are processed successfully
- Then the first task is assigned ID `n` and the second task is assigned ID `n+1`

---

**AC-007** — Mapped to FR-007 (Invalid Status Validation)

- Given a POST or PATCH request to `/tasks` or `/tasks/{id}` with a `status` value not in `[todo, in_progress, done]`
- When the request is processed
- Then the system returns HTTP 422 Unprocessable Entity

---

**AC-008** — Mapped to FR-008 (Unknown ID)

- Given a GET, PATCH, or DELETE request to `/tasks/{id}` where `{id}` does not correspond to an existing task
- When the request is processed
- Then the system returns HTTP 404 Not Found with the message `"Task with ID {id} does not exist"`

---

## 9. Assumptions

| ID   | Assumption | Basis |
|------|------------|-------|
| A-01 | The `status` field in a POST request is optional; when omitted, it defaults to `todo`. | Inferred from FR-007 ("Default: todo") in the JIRA data model. |
| A-02 | The DELETE response body is a JSON object containing a confirmation message (e.g., `{"message": "Task with ID {id} has been deleted"}`). The exact wording is not specified in JIRA. | AC-005 states "200 OK with confirmation message"; exact wording was not specified in JIRA. |
| A-03 | The PATCH response body is the full updated task object (all fields). | AC-004 states "200 OK"; returning the full updated object is standard REST practice and consistent with other endpoints. |
| A-04 | The GET /tasks endpoint returns an array at all times, including when no tasks exist (empty array `[]`), not a null or absent field. | Specified in FR-002 acceptance criteria. |
| A-05 | The `id` field is not accepted in the request body for POST or PATCH; it is always system-managed. | FR-006 states ID is "assigned by the system"; included here for implementer clarity. |

---

## 10. Dependencies

| Dependency | Notes |
|------------|-------|
| Python 3.x | Runtime for FastAPI and SQLite integration |
| FastAPI    | Web framework (NFR-001) |
| SQLite     | Embedded persistence layer (NFR-002); no separate service required |
| Pytest     | Test framework per CLAUDE.md project scope |

No external service dependencies. All components run locally.

---

## 11. Out of Scope

The following are explicitly excluded from this implementation per JIRA KAN-24:

- Authentication and authorization
- Multi-user support
- Filtering, search, or pagination on task lists
- Task priorities, due dates, tags, or attachments
- Notifications, email, or any cloud deployment
- Task history or audit trail

---

## 12. Requirements Traceability

| JIRA Story | Requirement ID | Acceptance Criteria | Description |
|------------|----------------|---------------------|-------------|
| KAN-24     | FR-001         | AC-001              | Create a task with title, description, and status; returns 201 with task object including id |
| KAN-24     | FR-002         | AC-002              | Retrieve all tasks; returns 200 with JSON array (empty array if none) |
| KAN-24     | FR-003         | AC-003              | Retrieve task by ID; returns 200 with task object when found |
| KAN-24     | FR-004         | AC-004              | Partially update task; only supplied fields updated; returns 200 with updated task |
| KAN-24     | FR-005         | AC-005              | Delete task by ID; returns 200 with confirmation message |
| KAN-24     | FR-006         | AC-006              | Auto-incremented integer IDs; sequential POSTs produce IDs n and n+1 |
| KAN-24     | FR-007         | AC-007              | Invalid status value returns 422 Unprocessable Entity |
| KAN-24     | FR-008         | AC-008              | Unknown task ID on GET/PATCH/DELETE returns 404 with standardized message |

---

## 13. Clarification Summary

### Questions Asked

The JIRA story KAN-24 is highly detailed and complete. No blocking clarifications were required. Two minor ambiguities were identified and resolved via documented assumptions:

| Question | Resolution |
|----------|------------|
| What is the exact body/wording of the DELETE 200 confirmation response? | Assumed a standard JSON confirmation message (see Assumption A-02). To be confirmed if exact wording matters for acceptance testing. |
| Does the PATCH endpoint return the full updated task object or only the changed fields? | Assumed full updated task object is returned (see Assumption A-03), consistent with standard REST practice. |

### Decisions Made

- All 8 functional requirements from JIRA are captured without modification.
- Acceptance criteria are expressed in Given/When/Then format, preserving the original JIRA intent.
- `status` defaults to `todo` when not supplied on task creation (A-01).
- No new requirements were introduced beyond what is in JIRA.

---

## 14. Approval Status

**Status: APPROVED**

Approved by human on 2026-10-17. Architecture stage may proceed.
