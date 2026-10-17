---
name: sdlc-test-verification
description: 'Create and execute pytest tests for approved acceptance criteria and report requirement-to-test evidence. Use for QA, test authoring, and verification.'
---

# Test Verification

1. Read approved requirements and inspect the implementation and existing test conventions.
2. Map applicable functional requirements and acceptance criteria to focused tests. Cover approved happy-path CRUD behavior where relevant; do not add unapproved scope.
3. Add or update tests under `tests/`, preferably reusing existing fixtures and test files.
4. Execute the relevant pytest command. Preserve actual output/status; if execution is blocked, state why and do not claim success.
5. Create `docs/plans/verification.md` with requirement ID, test name, actual result, and execution summary. Identify failures and untested requirements explicitly.