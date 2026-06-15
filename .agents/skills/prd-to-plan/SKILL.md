---
name: prd-to-plan
description: Convert an approved PRD into an actionable implementation plan with affected files, tasks, risks, specialists, and validation commands. Use after PRD intake and before any medium or large implementation work.
---

# PRD To Plan

Use this skill after `prd-intake` says the PRD is ready.

## Goal

Turn the PRD into an execution plan that is specific enough to implement without drifting.

## Inputs

- active PRD
- repo context from `pr_explorer`
- docs verification from `docs_researcher` when uncertainty exists

## Workflow

1. Restate the PRD goal, scope, non-goals, and platform target.
2. For delivery-oriented PRDs, restate delivery mode, reporting mode, secret profile, and human handoff assumptions.
3. Map the likely implementation area using existing repository patterns.
4. List the smallest affected files or directories that can satisfy the PRD.
5. Break the work into ordered tasks.
6. Identify risks, edge cases, dependencies, and any secret or delivery boundary that must stay external to the repo.
7. List validation commands that should run after the change.
8. Decide whether optional specialists are needed. Only include them when the PRD clearly requires them.
9. Mark user-approval-required work explicitly when the plan includes dependencies, migrations, auth changes, payment changes, file deletion, or new secret-bearing integrations.
10. Write the plan to `PLANS/`.

## Plan format

Every plan should include:

- source PRD
- status
- platform target
- affected files or directories
- tasks in execution order
- risks and edge cases
- validation commands
- review gates
- release or rollback notes when relevant

## Rules

- Do not implement while writing the plan.
- Keep the plan grounded in existing codebase patterns.
- Prefer small, reviewable steps over broad refactors.
- Call out approval-required work up front instead of burying it inside implementation tasks.
- If the PRD is medium or large, require explicit approval before implementation.
