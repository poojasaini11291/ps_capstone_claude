---
name: sdlc-workflow-audit
description: 'Audit completed and incomplete SDLC stages against artifacts, explicit approvals, Git history, and test output. Use to produce the final HTML execution report.'
---

# Workflow Audit

1. Read workflow context, all relevant `docs/plans/` artifacts, available Git history, and actual test evidence.
2. Verify each stage independently: artifact existence, status, approval evidence, test evidence, and completion history. Missing evidence is unverified, not successful.
3. Generate `docs/workflow-report-WF-2026-001.html`, using the recorded workflow ID if available.
4. Report completed, incomplete, blocked, and unverified stages; list deliverables, explicit approvals, actual test results, and evidence references.
5. Do not invent approvals, commits, tests, or stage completion. Report any inconsistency between workflow state and artifacts.