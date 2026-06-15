---
name: release-check
description: Run a final release-readiness checklist with validation status, rollout notes, rollback notes, and known risks. Use before merging or handing off a completed PRD-driven change.
---

# Release Check

Use this skill at the end of a PRD-driven task.

## Goal

Confirm that the implemented change is ready to hand off, merge, or release.

## Checklist

- PRD goal and acceptance criteria are satisfied
- scope and non-goals were respected
- validation commands were run and results are captured
- QA review completed
- security review completed
- docs or assumption verification completed when needed
- GitHub delivery status is clear, including whether the expected branch or PR handoff exists
- local handoff status is clear when reporting was part of scope
- secret handling stayed external to tracked files
- human handoff steps are captured clearly for QA, release approval, and operational follow-up
- release risks and monitoring notes are captured when relevant
- rollback or revert path is understood

## Output

Return:

- release status: `ready`, `ready-with-risks`, or `blocked`
- validations run
- outstanding risks
- rollback notes
- follow-up items

## Rules

- Do not invent release confidence if validations were skipped.
- If required validations were not run, the change is not `ready`.
- If operational or migration risk exists, involve `release_specialist`.
