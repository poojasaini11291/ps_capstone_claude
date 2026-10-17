---
name: sdlc-workflow-orchestration
description: 'Start or resume the full agentic SDLC by delegating to specialist agents in dependency order and enforcing human approval gates.'
---

# SDLC Workflow Orchestration

1. Read `.github/copilot-instructions.md`, `context/workflow-context.json` if present, and the available project artifacts. Resume from verified state; do not redo or skip work based on assumptions.
2. Run stages in order and delegate to the named agent: business analyst; solution architect; solution engineer; branch/git planner; developer; code reviewer; automation tester; deploy/build engineer; chronicle auditor.
3. Requirements stage: obtain a JIRA key/URL, retrieve the real story, clarify ambiguity, produce requirements, and stop for approval.
4. Architecture and design review follow approved requirements. Planning follows review; produce the plan and stop for explicit approval. Do not start production implementation before approval.
5. Delegate implementation, then code review. Return blockers to the developer and repeat review until resolved. Delegate verification and require actual passing tests before release.
6. Delegate release preparation. Get explicit approval before PR creation; after final PR review, require explicit approval before merge.
7. After each stage, verify its expected artifact and update workflow context with actual results, approvals, and history. Never record an unverified outcome.
8. Stop whenever user input/approval or an unavailable integration/agent blocks progress. Report completed stages, artifacts, blockers, and the next required decision.
9. Delegate the workflow audit after other stages and produce the final HTML report from verified evidence only.