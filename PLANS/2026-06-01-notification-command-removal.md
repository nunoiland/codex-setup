# Plan: Notification command removal

## Source PRD
- `PRD/2026-06-01-notification-command-removal.md`

## Status
- Approved for implementation

## Platform target
- codex-setting runtime and docs

## Summary
Remove the retired external notification command and notification surface from active runtime, docs, environment examples, historical artifacts, and validation. Preserve GitHub-first delivery, local handoff rendering, queue worker, cron queue processing, harness evidence, Product Factory, design layer, and external opt-in tooling.

## Affected files or directories
- `codex_runtime/`, `scripts/`, `.env.example`, `.codex/`, `docs/`, `PRD/`, `PLANS/`, `README.md`, `AGENTS.md`

## Implementation tasks
1. Add this PRD and plan.
2. Remove retired command polling runtime and exports.
3. Convert reporting to local handoff rendering only.
4. Simplify CLI and cron runner to queue and local handoff flows.
5. Remove retired env variables, docs, templates, examples, and historical artifacts.
6. Add validation that active tracked files do not reintroduce retired notification keywords.
7. Run validation, CI check, readiness, handoff rendering, and queue cron smoke checks.

## Guardrails
- No dependencies, services, secrets, auth, billing, deployment, or migrations.
- Do not weaken GitHub-first or protected-branch safety.
- Do not remove queue, memory, Product Factory, Hermes/Paperclip/Graphiti readiness, design, or external opt-in pattern contracts.
- Ignore stale local runtime state instead of migrating it.

## Validation commands
```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
python3 -m codex_runtime --prd PRD/2026-04-11-example-product-prd-web-ios.md --prepare-reporting --cwd . --pretty
CODEX_CRON_LOG_FILE=- CODEX_CRON_MODE=queue CODEX_CRON_MAX_RUNS=1 CODEX_CRON_MAX_IDLE_CYCLES=1 CODEX_CRON_POLL_SECONDS=0 ./scripts/cron-runner.sh
```

## Review gates
- QA review for queue, local handoff, and validation behavior.
- Security review for removed secret surface and no new credentials.
- Docs review for discoverability and no stale retired-notification references.

## Risks
- Old run records may keep stale keys; current code should ignore them.
- Removing historical docs reduces archived context, but this is intentional to prevent the retired surface from appearing supported.
- Future operator console work must start from a new PRD.
