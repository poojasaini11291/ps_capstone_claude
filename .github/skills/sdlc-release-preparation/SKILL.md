---
name: sdlc-release-preparation
description: 'Prepare release notes and a GitHub pull request using completed review and actual passing test evidence. Use for release readiness and PR drafting.'
---

# Release Preparation

1. Confirm implementation and code review are complete and verification contains executed passing test evidence. Stop if prerequisites are missing or blockers remain.
2. Review deliverables, summarize changes, record known limitations, and prepare a changelog when appropriate.
3. Draft the PR description with sections: Summary, Changes Made, Test Evidence, Known Limitations, Reviewer Checklist.
4. Ask for explicit user approval before creating a PR. Do not infer approval from a draft or prior checkpoint.
5. After a PR is available, present it for final human review. Require a separate explicit approval before merge; never merge without it.
6. Report only actual GitHub and test outcomes. Do not claim tests passed unless executed.