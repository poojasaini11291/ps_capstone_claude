---
name: sdlc-implementation-planning
description: 'Break approved requirements and architecture into ordered, dependency-aware implementation tasks with files and a branch suggestion. Use before development.'
---

# Implementation Planning

1. Read approved requirements, architecture, and design review. Resolve missing prerequisites before planning.
2. Break the work into small, verifiable tasks with stable IDs, dependencies, and expected files. Order tasks so dependencies precede consumers.
3. Include a recommended feature branch name; recommend only, do not create it.
4. Create `docs/plans/impl-plan.md` and identify verification points for each relevant task.
5. Do not implement application code. Present the plan and stop for explicit human approval. Record approval only after it is given.