---
name: implement-from-plan
description: Execute only an approved implementation plan. Use when a PRD-backed plan already exists and Codex must apply the smallest aligned code change, route work to the correct platform area, and run validation after edits.
---

# Implement From Plan

Use this skill only when there is an approved plan.

## Preconditions

- A PRD has been read.
- The plan exists and is approved.
- The affected platform area is known.
- For delivery-oriented work, the PRD defines delivery mode, reporting mode, secret profile, and human handoff.

## Workflow

1. Re-read the PRD and the approved plan.
2. Confirm the platform area and affected files.
3. For delivery-oriented work, confirm what must stay outside the repository, especially secrets, runtime credentials, and external reporting configuration.
4. Reuse existing patterns before introducing any new abstractions.
5. Implement one planned task at a time.
6. Keep diffs small and local.
7. Run the plan's validation commands after code changes.
8. If implementation reveals a material scope change, stop and update the plan before continuing.

## Routing

- Use `web_builder` for web work.
- Use `android_builder` for Android work.
- Use `ios_builder` for iOS work.
- Use `api_builder` for backend and API work.
- Use specialists only when the plan explicitly calls for them.

## Rules

- Never skip directly from PRD to implementation for medium or large work.
- Do not change unrelated files.
- Do not expand scope beyond the approved plan.
- Keep GitHub delivery assumptions aligned with the PRD and plan; do not silently switch from branch-plus-PR delivery to direct protected-branch pushes.
- Never commit secrets, tokens, webhook URLs, or bot credentials.
- Treat marketing, pricing, and revenue outputs as drafts for human review rather than authoritative decisions.
- Ask before adding dependencies, creating or applying migrations, making auth changes, making payment changes, or deleting files.
- Never claim success unless validation commands were actually run.
- If validation fails, fix it or report the exact blocker before finalizing.
