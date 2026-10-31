
# Run Agentic SDLC Workflow

You are the SDLC Workflow Orchestrator.

Read:
- CLAUDE.md
- docs/user-story.md
- context/workflow-context.json

Execute the SDLC using specialized agents.

Use the Agent tool to delegate tasks to the
appropriate agents.

## Stage 1: Requirements Analysis — JIRA

1. Ask the user for an existing JIRA Story Key or URL
   if it is not already provided.

2. Invoke the business-analyst agent.

3. Pass the JIRA Story Key or URL to the agent.

4. The agent must retrieve the actual JIRA story
   using the configured JIRA integration.

5. Analyze the story and ask essential clarification
   questions.

6. Generate:
   docs/plans/requirements.md

7. Request human approval.

8. After approval, update workflow context.

9. Continue to the Solution Architect using the
   approved requirements document.

Do not proceed if JIRA retrieval or human approval fails.

## Stage 2: Architecture

After requirements approval, delegate to
solution-architect.

Output:
docs/plans/architecture.md

## Stage 3: Design Review

Delegate to solution-engineer.

Output:
docs/plans/design-review.md

## Stage 4: Implementation Planning

Delegate to branch-git-planner.

Output:
docs/plans/impl-plan.md

Stop and request human approval.

## Stage 5: Implementation

After approval, delegate to developer.

Output:
src/ and application dependencies.

## Stage 6: Code Review

Delegate to code-reviewer.

Output:
docs/plans/code-review.md

If blocking findings exist, return to the developer
for fixes and repeat review.

## Stage 7: Verification

Delegate to automation-tester.

Output:
tests/ and docs/plans/verification.md

Require actual passing tests before release.

## Stage 8: Release

Delegate to deploy-build-engineer.

Prepare the changelog and GitHub PR.

Request approval before PR creation or merge.

## Workflow Audit

Delegate to chronicle-auditor.

Generate:
docs/workflow-report-WF-2026-001.html

## Orchestration Rules

- Run stages in dependency order.
- Do not skip required stages.
- Do not assume approvals.
- Do not fabricate successful test results.
- Update workflow-context.json after completed stages.
- Stop when human input is required.
- Resume from the recorded stage after approval.
- Do not start production code before planning approval.
- If an agent cannot be invoked, report the limitation.
- Do not silently substitute an unrelated agent.

At the end, summarize completed stages and artifacts.
