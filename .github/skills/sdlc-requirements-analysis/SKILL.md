---
name: sdlc-requirements-analysis
description: 'Retrieve and analyze an existing JIRA story, resolve essential ambiguity, and create traceable requirements. Use for requirements discovery, acceptance criteria, or requirements approval.'
---

# Requirements Analysis

1. Read `.github/copilot-instructions.md`, the workflow context if present, and the business analyst instructions.
2. Obtain a JIRA story key or URL. Discover an available configured JIRA read integration; do not assume its tool name. If no integration exists, stop and explain the blocker. Never ask for credentials in chat.
3. Retrieve and verify the requested story. Capture key, URL, summary, description/user story, acceptance criteria, priority, status, labels, linked issues, and dependencies. Mark absent fields `Not provided in JIRA`; do not modify JIRA.
4. Analyze objective, functional and minimal non-functional requirements, acceptance criteria, assumptions, dependencies, and out-of-scope items. Preserve additional scenarios from JIRA and flag scope questions rather than dropping them.
5. Ask grouped, essential clarification questions. Wait for answers before finalizing; distinguish confirmed facts from assumptions.
6. Create `docs/plans/requirements.md` with: JIRA details; objective; original story; numbered requirements (`FR-001`...); non-functional requirements; numbered Given/When/Then criteria (`AC-001`...); assumptions; dependencies; out of scope; traceability table; clarification summary; approval status.
7. Map each functional requirement to acceptance criteria and the originating story. Set `Status: AWAITING HUMAN APPROVAL`.
8. Present story key, concise summary, requirement/criteria counts, assumptions, missing information, and file path. Stop for explicit approval. Only after approval, mark approved and record the approval in context when available.