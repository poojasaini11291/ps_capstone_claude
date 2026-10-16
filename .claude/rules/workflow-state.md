
# Workflow State Rules

Use context/workflow-context.json to record SDLC progress.

After completing a stage:

1. Confirm the expected artifact exists.
2. Record the stage result.
3. Update current_stage.
4. Record any verified test results.
5. Record approval only after explicit human confirmation.
6. Append an execution history entry.

Never:
- Invent approvals.
- Mark unfinished stages as completed.
- Record tests as passed without execution.
- Skip mandatory approval checkpoints.
