# Product Factory Goal Contract

Use `/goal` as the human-facing starting point for any new product, feature, growth experiment, or operational improvement.

`/goal` is not an autonomous permission to ship. It is an intake format that becomes a PRD, then a plan, then local Codex app implementation, then GitHub Actions validation.

## Required shape

```text
/goal
Goal:
Product:
Success criteria:
Target platforms:
Constraints:
Validation commands:
Approval boundary:
```

## Default flow

1. Convert `/goal` into a PRD under `PRD/`.
2. Create or update a plan under `PLANS/`.
3. Implement locally with the Codex app.
4. Run local validation.
5. Open a PR.
6. Let API-key-free GitHub Actions collect evidence.
7. Update memory with decisions, failures, QA risks, and next actions.

## Minimum acceptance criteria

Every `/goal` must make these explicit:

- what user or business outcome should improve
- which product or repository is affected
- how success will be measured
- which platforms are in scope
- what is not allowed without approval
- which commands prove the result

## Paperclip mapping

When Paperclip is enabled later:

- `/goal` maps to a Paperclip goal or issue.
- The assigned worker may be local Codex, Hermes, or another approved agent.
- Paperclip may track approvals, budgets, and audit logs.
- GitHub remains the merge and validation source of truth.

## Safety defaults

- Do not include secrets in `/goal`.
- Do not request direct protected-branch pushes.
- Do not ask workers to bypass tests, review, or approval gates.
- Treat revenue, launch, and strategy output as human-reviewed drafts.
