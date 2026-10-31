---
name: sdlc-design-review
description: 'Review an architecture against approved requirements for completeness, simplicity, API design, responsibilities, and data flow. Use before implementation planning.'
---

# Design Review

1. Read approved requirements and `docs/plans/architecture.md`.
2. Check requirement coverage, component ownership, simplicity, endpoint behavior, data model, and end-to-end data flow. Identify unsupported scope and missing decisions.
3. Create `docs/plans/design-review.md` with review summary, requirement coverage, evidence-based findings, agreed design decisions, and final review status.
4. Recommend concrete changes. Update `architecture.md` only if needed, and record the change in the review.
5. Do not implement application code. Report blockers and completion to the orchestrator.