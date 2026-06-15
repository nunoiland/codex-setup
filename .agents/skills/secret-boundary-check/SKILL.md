---
name: secret-boundary-check
description: Verify that a PRD-driven run keeps all secrets outside tracked files, documents the source of injection, and stops or flags blockers when required credentials are missing. Use for delivery, reporting, auth-sensitive, or integration-heavy work.
---

# Secret Boundary Check

Use this skill whenever the task touches GitHub delivery, provider keys, local handoff reporting, deployment credentials, or any other runtime secret.

## Goal

Make secret handling explicit and keep credentials outside the repository.

## Inputs

- active PRD
- approved plan when available
- current diff or proposed file changes
- reported secret requirements from delivery or reporting integrations

## Workflow

1. Read the PRD and find the `Secret profile` section.
2. Confirm each required secret has:
   - a clear purpose
   - an external source of injection
   - an owner or approver
3. Review the current diff or proposal for tracked secret exposure.
4. Check whether placeholders are used instead of real values in examples and docs.
5. Call out any missing credential source, owner, or runtime boundary as a blocker.
6. Summarize whether the change is safe to continue from a secret-boundary perspective.

## Output shape

Return:

- status: `ok`, `ok-with-risks`, or `blocked`
- required secrets
- source of injection
- owner or approver
- tracked-file exposure findings
- blockers and follow-up actions

## Rules

- Never accept real secrets in tracked files.
- Treat webhook URLs and service tokens as secrets.
- Prefer least-privilege guidance over convenience.
- If ownership or injection source is missing for a required credential, call it out explicitly.
