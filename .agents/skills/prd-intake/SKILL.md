---
name: prd-intake
description: Validate a PRD before planning or implementation. Use when a task starts from a PRD and Codex must check completeness, identify missing fields, classify size, and stop unsafe implementation starts.
---

# PRD Intake

Use this skill at the start of any PRD-driven task.

## Goal

Confirm that the PRD is usable, identify missing information, and decide whether implementation can proceed to planning.

## Required sections

Every PRD must include:

- Goal
- Scope
- Non-goals
- Context
- Constraints
- Acceptance criteria
- Edge cases
- Platform target
- Validation commands
- Done when

For product-generation or unattended-delivery PRDs, also require:

- Delivery mode
- Reporting mode
- Secret profile
- Human handoff

## Workflow

1. Read the PRD before inspecting code.
2. Summarize the requested user outcome in 3 to 6 lines.
3. Check each required section for completeness and specificity.
4. If the PRD involves product delivery or overnight execution, verify delivery mode, reporting mode, secret profile, and human handoff.
5. Classify the task:
   - Small: local, single area, low ambiguity
   - Medium: multi-file or moderate ambiguity
   - Large: cross-cutting, multi-platform, migration-heavy, or high-risk
6. If anything critical is missing, stop and list the missing information clearly.
7. If the PRD is complete, state whether planning is mandatory. Planning is mandatory for medium and large tasks.

## Output shape

Return:

- PRD readiness: `ready` or `blocked`
- task size: `small`, `medium`, or `large`
- platform target
- delivery and reporting summary when relevant
- missing information
- key acceptance criteria
- key risks or ambiguities
- next step

## Rules

- Do not implement during intake.
- Do not rewrite the PRD unless the user asks.
- If the PRD conflicts with repo reality, flag it before planning.
