
# Requirements Document
## Task Management REST API

**Workflow ID:** WF-2026-001
**Stage:** Requirements
**Author:** Business Analyst Agent
**Date:** 2026-10-17

---

## 1. Project Objective

Build a simple Task Management REST API that allows users to create, view, update, and delete tasks. The API must persist tasks using SQLite and expose a clean REST interface via FastAPI.

---

## 2. User Story

> As a user,
> I want to create, view, update and delete tasks,
> so that I can manage my daily activities.

---

## 3. Functional Requirements

| ID     | Requirement                                                                 |
|--------|-----------------------------------------------------------------------------|
| FR-001 | The system shall allow a user to create a task with title, description, and status. |
| FR-002 | The system shall return a list of all tasks.                                |
| FR-003 | The system shall return a single task by its ID.                            |
| FR-004 | The system shall allow a user to partially update a task (title, description, or status individually or in combination). |
| FR-005 | The system shall allow a user to delete a task by its ID.                   |
| FR-006 | Each task shall have an auto-incremented integer ID assigned by the system. |
| FR-007 | Task status shall be restricted to the values: `todo`, `in_progress`, `done`. |
| FR-008 | When a task ID does not exist, the system shall return a 404 response with a message stating the task does not exist. |

---

## 4. Data Model

### Task

| Field       | Type    | Required | Notes                                      |
|-------------|---------|----------|--------------------------------------------|
| id          | integer | system   | Auto-incremented, assigned on create       |
| title       | string  | yes      | Provided by user                           |
| description | string  | yes      | Provided by user                           |
| status      | string  | yes      | One of: `todo`, `in_progress`, `done`. Default: `todo` |

---

## 5. API Endpoints

| Method | Path           | Description              |
|--------|----------------|--------------------------|
| POST   | /tasks         | Create a new task        |
| GET    | /tasks         | Retrieve all tasks       |
| GET    | /tasks/{id}    | Retrieve a task by ID    |
| PATCH  | /tasks/{id}    | Partially update a task  |
| DELETE | /tasks/{id}    | Delete a task by ID      |

---

## 6. Non-Functional Requirements

| ID      | Requirement                                                             |
|---------|-------------------------------------------------------------------------|
| NFR-001 | The API shall be implemented using Python and FastAPI.                  |
| NFR-002 | Data shall be persisted using SQLite.                                   |
| NFR-003 | The API shall return JSON responses.                                    |
| NFR-004 | The application shall run locally without external infrastructure.      |

---

## 7. Acceptance Criteria

### FR-001 — Create Task
- **Given** a POST request to `/tasks` with valid `title`, `description`, and `status`
- **When** the request is processed
- **Then** the system returns `201 Created` with the new task including its assigned `id`

### FR-002 — View All Tasks
- **Given** a GET request to `/tasks`
- **When** the request is processed
- **Then** the system returns `200 OK` with a JSON array of all tasks (empty array if none exist)

### FR-003 — View Task by ID
- **Given** a GET request to `/tasks/{id}` where the task exists
- **When** the request is processed
- **Then** the system returns `200 OK` with the task object

### FR-004 — Partial Update
- **Given** a PATCH request to `/tasks/{id}` with one or more fields (`title`, `description`, `status`)
- **When** the request is processed
- **Then** the system returns `200 OK` with the updated task; unspecified fields remain unchanged

### FR-005 — Delete Task
- **Given** a DELETE request to `/tasks/{id}` where the task exists
- **When** the request is processed
- **Then** the system returns `200 OK` with a confirmation message

### FR-006 — Auto-incremented ID
- **Given** two sequential POST requests to `/tasks`
- **When** both are processed
- **Then** the second task has an `id` exactly one greater than the first

### FR-007 — Status Validation
- **Given** a POST or PATCH request with a `status` value outside `todo`, `in_progress`, `done`
- **When** the request is processed
- **Then** the system returns `422 Unprocessable Entity`

### FR-008 — Task Not Found
- **Given** a GET, PATCH, or DELETE request to `/tasks/{id}` where no task with that ID exists
- **When** the request is processed
- **Then** the system returns `404 Not Found` with a message: `"Task with ID {id} does not exist"`

---

## 8. Assumptions

- A single user operates the API locally; no authentication is required.
- The SQLite database file is created automatically on first run.
- Default status for a newly created task is `todo`.
- The API does not need to support pagination or filtering.

---

## 9. Out of Scope

- User authentication or authorization
- Multi-user support
- Task filtering or search
- Task priorities, due dates, tags, or attachments
- Notifications or email
- Deployment to cloud infrastructure
- API versioning

---

## 10. Approval Status

**Status: AWAITING HUMAN APPROVAL**

Please review the requirements above and confirm approval to proceed to architecture design.
