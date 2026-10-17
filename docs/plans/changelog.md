# Changelog

## Unreleased

- Replaced the active Task Management API entry point with a local calculator web application.
- Added decimal arithmetic for addition, subtraction, multiplication, and division through `POST /calculate`.
- Added the calculator UI with Calculate and Clear actions; Clear resets the operation to Addition.
- Removed SQLAlchemy runtime dependency and task-specific API tests. Preserved the existing local database file.
- Added calculator API and static-page tests; all 7 tests pass.