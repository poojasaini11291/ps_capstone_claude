# Pull Request Draft

## Summary

Implement KAN-25 as a locally runnable Calculator Web Application using FastAPI and a static HTML/CSS/JavaScript frontend.

## Changes Made

- Added stateless decimal calculation logic and `POST /calculate` for the four basic operations.
- Added the calculator UI, responsive styling, and Calculate/Clear behavior.
- Removed active Task API wiring and SQLAlchemy runtime dependency; preserved `src/tasks.db`.
- Replaced Task API tests with calculator and static-asset tests and documented local setup.

## Test Evidence

- `python -m pytest -q`: 7 passed, 0 failed.
- Browser checked addition with decimal operands and verified Clear restores Addition and empties both inputs and the result.
- Local Uvicorn app loaded successfully at `http://127.0.0.1:8000/`.

## Known Limitations

- Two upstream Starlette/httpx TestClient deprecation warnings appear during pytest.
- Clear behavior is browser-verified but not covered by automated browser tests.

## Reviewer Checklist

- [ ] Confirm acceptance criteria and operation results.
- [ ] Confirm no database is required at runtime.
- [ ] Confirm local run instructions and test evidence.

## Approval Status

PR #3 is open from `feature/KAN-25-calculator` into `main`: https://github.com/poojasaini11291/ps_capstone_claude/pull/3. Final human review and separate approval before merge are pending.