# Product Factory Operating Model

This is the operating model for using `codex-setting` as the base template repo for many web, app, and backend products.

## Default loop

1. Capture the work as `/goal`.
2. Convert the goal into a PRD.
3. Select the service basecamp contract when the goal creates or changes a product service.
4. Start from the included product starter, then use the local Codex app or Hermes worker to plan, implement, review, and fix.
5. Open a GitHub PR.
6. Let API-key-free GitHub Actions run validation and harness evidence collection.
7. Feed failures back into local Codex or Hermes with the uploaded harness artifact.
8. Merge only after required checks pass and a human applies the approved merge label.
9. Store run results, decisions, QA risks, revenue lessons, and next tasks into the memory layer.

## Operator platform direction

Paperclip is the preferred future operator dashboard for:

- product goals
- task tickets
- agent assignment
- approval gates
- budgets
- audit logs
- recurring routines

Paperclip is not required for normal PR validation. Missing Paperclip configuration should appear as readiness output, not a validation failure.

## Worker direction

Hermes is the preferred future managed worker target because it provides persistent memory, skills, sub-agents, MCP, and multiple model providers. In this repository phase, Hermes is a contract target only.

The current default remains:

- local Codex app for implementation
- local JSON runtime state for memory
- GitHub Actions for non-AI validation

## Product quality expectations

Every product created from this setup should preserve:

- PRD-first scope control
- branch and PR delivery
- repeatable validation
- explicit evidence artifacts
- secret-free tracked files
- product-state memory
- service basecamp contracts for deployment, revenue, admin, logging, backup, and restore
- human approval before production-sensitive changes

## Readiness command

Use:

```bash
python3 -m codex_runtime --operator-readiness --pretty
```

This command reports optional Product Factory services without requiring them.

For the goal intake shape, use [`product-factory-goal-contract.md`](./product-factory-goal-contract.md).
For optional setup risks, use [`product-factory-risk-register.md`](./product-factory-risk-register.md).
For future service creation, use [`service-basecamp-architecture.md`](./service-basecamp-architecture.md).
