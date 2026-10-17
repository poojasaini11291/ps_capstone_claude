
# Changelog
## Task Management REST API — v1.0.0

**Date:** 2026-10-17
**Branch:** feature/task-management-api
**Workflow ID:** WF-2026-001

---

## What's New

### Task Management REST API (initial release)

A fully functional CRUD REST API for managing tasks, built with Python, FastAPI, and SQLite.

#### Features

- **Create task** — `POST /tasks/` with title, description, and optional status (defaults to `todo`)
- **List all tasks** — `GET /tasks/` returns a flat JSON array of all tasks
- **Get task by ID** — `GET /tasks/{id}` returns a single task or 404 if not found
- **Partial update** — `PATCH /tasks/{id}` updates only the fields provided; unspecified fields unchanged
- **Delete task** — `DELETE /tasks/{id}` removes the task and returns a confirmation message

#### Data Model

Each task has:
- `id` — auto-incremented integer, system-assigned
- `title` — required string
- `description` — required string
- `status` — one of `todo`, `in_progress`, `done` (default: `todo`)

#### Error Handling

- Invalid status value → `422 Unprocessable Entity`
- Task ID not found → `404 Not Found` with message `"Task with ID {id} does not exist"`

---

## Pull Request

**PR #1 — feat: Task Management REST API — initial implementation**
https://github.com/poojasaini11291/ps_capstone_claude/pull/1
Merged to `main` · Merge commit: `8138961`

---

## Commits

| Hash | Message |
|------|---------|
| `8138961` | feat: Task Management REST API — initial implementation (#1) |
| `d837de5` | test: add pytest suite and verification report — 15/15 passing |
| `4fdd348` | chore: exclude SQLite database file from version control |
| `da031c0` | feat: implement Task Management REST API |

---

## Known Limitations

- No authentication or authorization (out of scope)
- No pagination or filtering (out of scope)
- Single-user, local deployment only
- SQLite not suitable for concurrent production workloads
- No API versioning

---

## Test Evidence

**15/15 tests passed** — pytest 9.1.1, Python 3.11.9, 2026-10-17

All 8 functional requirements verified. See `docs/plans/verification.md` for full traceability matrix.
