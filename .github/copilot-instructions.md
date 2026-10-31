# Agentic SDLC Project

## Objective

Build and operate a small agent-assisted SDLC workflow for the KAN-25 Calculator Web Application using Python, FastAPI, HTML, CSS, JavaScript, and pytest. The application runs locally and does not use a database. Keep implementation focused on approved requirements and happy-path behavior; do not add frameworks, services, or features without approval.

## Source Of Truth

- For requirements work, use the actual JIRA story retrieved through an integration available in the current environment. A story key or URL must be supplied by the user or recorded in `context/workflow-context.json`.
- Do not treat `docs/user-story.md` as authoritative. Do not invent JIRA details, integration results, approvals, commits, or test results.
- If the required JIRA integration is unavailable, explain the limitation and stop requirements analysis.
- Read `context/workflow-context.json` when it exists, and keep it consistent with completed work and explicit approvals.

## Workflow And Approval Gates

Follow the stages in order: requirements, architecture, design review, implementation plan, implementation, code review, verification, release/PR, and workflow audit. Use the matching custom agents and skills under `.github/` for role-specific work.

Human approval is mandatory after requirements, after the implementation plan, before creating a GitHub PR, and after final PR review before merge. Stop at each gate until the user explicitly approves. Never infer approval from silence or prior approvals.

Do not begin production implementation before the approved implementation plan. Resolve blocker findings before verification/release. Require executed, passing tests before release. Do not merge a PR without explicit human approval.

## Deliverables

- SDLC plans and reviews: `docs/plans/`
- Application: `src/` (FastAPI backend and static frontend assets)
- Tests: `tests/`
- Verification: `docs/plans/verification.md`
- Workflow state: `context/workflow-context.json`
- Final audit: `docs/workflow-report-WF-2026-001.html` (use the workflow ID recorded in context if it differs)

Each agent must read its relevant inputs, perform only its assigned role, create or update the expected artifact, report completion and evidence, and update workflow context only when appropriate. Preserve existing user changes and avoid unrelated cleanup.

## Quality And Safety

- Prefer the simplest design that satisfies approved requirements.
- Review code for correctness, requirements traceability, readability, architecture alignment, obvious security issues, and happy-path coverage.
- Run relevant tests before reporting success; state the exact check and result.
- Keep secrets out of source, logs, artifacts, and conversation. Never request credentials in chat.
- Do not perform irreversible GitHub actions or merge changes without the required explicit approval.