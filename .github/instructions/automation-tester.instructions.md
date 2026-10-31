---
description: Use when creating or running pytest tests, verifying acceptance criteria, or preparing verification.md.
---

# QA Automation Instructions

- Derive tests from requirement and acceptance-criterion IDs; prioritize happy-path create/read/update/delete behavior where approved.
- Add focused pytest coverage under `tests/` and execute it in the project environment.
- Create `docs/plans/verification.md` mapping requirement ID, test name, actual result, and execution summary.
- Record failures and untested requirements accurately; never infer a pass from test code or stale output.