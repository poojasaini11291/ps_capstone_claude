
# Agentic SDLC Capstone Project

## Objective

Implement a complete Agentic SDLC pipeline using Claude Code.

The pipeline must cover:
1. Requirements Analysis
2. Architecture Design
3. Design Review
4. Implementation Planning
5. Development
6. Code Review
7. Verification
8. GitHub Pull Request

## Application

Build a simple Task Management REST API.

Technology:
- Python
- FastAPI
- SQLite
- Pytest
- GitHub

## Project Scope

Focus on happy-path scenarios only.

Do not introduce unnecessary features, frameworks,
microservices, cloud infrastructure, or complexity.

## Workflow

Use the agents defined in .claude/agents/.

Save SDLC deliverables under docs/plans/.

The workflow entry point is:
.claude/commands/run-sdlc-workflow.md

## Human Approval

Human approval is mandatory after:
- Requirements analysis
- Implementation planning
- Final PR review

Do not proceed through an approval checkpoint
without explicit user confirmation.

## Agent Execution

Each agent must:
1. Read relevant input documents.
2. Perform its assigned responsibility.
3. Create the expected output artifact.
4. Report what was completed.
5. Update workflow context when appropriate.

Do not fabricate successful executions or approvals.

## Quality

- Follow approved requirements.
- Keep code simple and readable.
- Write happy-path tests.
- Run tests before preparing a PR.
- Never expose secrets.
- Do not claim tests passed unless executed.

## Final Output

The final result must include:
- Requirements
- Architecture
- Design review
- Implementation plan
- Source code
- Test results
- Code review
- Verification report
- GitHub PR
- Workflow execution report
