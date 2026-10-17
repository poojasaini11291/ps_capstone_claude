---
name: sdlc-code-review
description: 'Review implementation against requirements and architecture for correctness, quality, security, and test coverage. Use after development; reviewer must not fix code.'
---

# Code Review

1. Read approved requirements, architecture, implementation plan, source, relevant tests, and available change evidence.
2. Review traceability, correctness, readability, duplication, architectural fit, obvious security issues, and happy-path coverage.
3. Report only substantiated, actionable findings with file/line evidence. Classify each `BLOCKER`, `MAJOR`, or `MINOR`, and state the impact and a concrete correction.
4. Create `docs/plans/code-review.md` with summary, findings, and review status. If there are no findings, say so explicitly.
5. Do not edit implementation code. Send blockers back for correction and repeat review after changes.