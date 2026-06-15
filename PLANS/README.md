# Plans Directory

Use `PLANS/` for approved implementation plans derived from PRDs.

## When to create a plan

- Always after reading a PRD
- Always for medium or large tasks
- Always for cross-platform, migration, auth, payment, or release-sensitive work
- Optionally for small tasks when the scope is still ambiguous

## Naming

Use a stable, readable filename such as:

- `PLANS/2026-04-03-add-checkout-discount-code.md`
- `PLANS/2026-04-03-mobile-session-refresh.md`
- `PLANS/2026-04-03-api-bulk-export.md`

## Required sections

Every plan should include:

- Source PRD
- Status
- Platform target
- Affected files or directories
- Implementation tasks
- Risks and edge cases
- Validation commands
- Review gates
- Release or rollback notes when relevant

For unattended product-delivery work, also capture delivery assumptions, reporting expectations, and secret boundaries in the tasks or risks sections.

## Suggested template

```md
# Plan: <short title>

## Source PRD
- `PRD/<file>.md`

## Status
- Draft
- Approved
- In progress
- Complete

## Platform target
- web | android | ios | api | multi-platform

## Affected files or directories
- path
- path

## Tasks
1. Task
2. Task
3. Task

## Risks and edge cases
- risk
- risk

## Validation commands
```bash
<command>
```

## Review gates
- QA review
- Security review
- Docs verification if assumptions were uncertain

## Release and rollback notes
- release note
- rollback note
```

## Rules

- The plan is the execution boundary. If scope changes materially, update the plan before continuing.
- Keep tasks ordered and concrete enough that a builder agent can execute them without guessing.
- Prefer the smallest change surface that satisfies the PRD.
