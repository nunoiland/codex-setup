---
name: morning-handoff
description: Produce a GitHub-first overnight handoff with platform status, validation results, manual follow-up, and draft product, marketing, and revenue strategy summaries. Use after implementation or unattended runs when a human will review the work in the morning.
---

# Morning Handoff

Use this skill near the end of an unattended or delivery-oriented run.

## Goal

Create a handoff that is reviewable, honest, and useful for a human operator starting the next work session.

## Inputs

- active PRD
- approved plan
- GitHub delivery status
- validation results
- platform-by-platform completion status
- missing secrets or delivery blockers

## Workflow

1. Re-read the PRD and approved plan.
2. Confirm the platform target, delivery mode, reporting mode, and human handoff expectations.
3. Summarize GitHub artifacts first: repo, branch, PR, and validation status.
4. Summarize success, partial success, or failure by platform.
5. List blockers, missing secrets, or skipped validations explicitly.
6. Add a concise QA checklist and manual follow-up list.
7. Add draft product, marketing, pricing, and revenue ideas only as drafts for human review.
8. Produce local handoff output that links back to GitHub artifacts when available.

## Output shape

Return:

- overall status
- GitHub artifacts
- platform status
- validations run
- blockers and missing secrets
- QA checklist
- manual follow-up
- product/marketing/revenue drafts
- local handoff summary when relevant

## Rules

- GitHub is the source of truth; local handoff output is only a summary.
- Never hide failed or skipped validations.
- Never invent delivery artifacts that do not exist.
- Treat strategy output as draft guidance, not final business direction.
