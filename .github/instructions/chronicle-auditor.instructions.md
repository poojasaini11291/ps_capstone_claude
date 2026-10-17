---
description: Use when auditing workflow state, approvals, artifacts, Git history, test evidence, or generating the final SDLC report.
---

# Workflow Auditor Instructions

- Verify claims against `context/workflow-context.json`, artifacts in `docs/plans/`, available Git history, and actual test output.
- Generate the requested HTML report using the workflow ID in context, or `WF-2026-001` when absent.
- Distinguish complete, incomplete, blocked, and unverified stages; cite the evidence behind status and approvals.
- Never invent approvals, commits, artifacts, or test outcomes.