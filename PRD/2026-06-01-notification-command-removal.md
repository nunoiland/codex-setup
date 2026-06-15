# Notification Command Removal PRD

## Goal
Simplify codex-setting by removing the retired external notification command and notification surface from runtime code, docs, environment examples, templates, and validation while preserving GitHub-first delivery, local handoff artifacts, queue processing, harness evidence, and Product Factory contracts.

## Scope
- Remove the retired notification command runtime and bot polling code.
- Make reporting a local GitHub-first handoff renderer only.
- Keep queue worker and cron queue processing.
- Remove retired notification environment variables, docs, examples, and historical artifacts from the active repository.
- Add validation that prevents the retired notification surface from reappearing.

## Non-goals
- No new dependencies, external services, credentials, deployment changes, auth changes, payment changes, migrations, or production rollout.
- Do not remove GitHub delivery, queue processing, Product Factory docs, Hermes/Paperclip/Graphiti contracts, design layer, external pattern layer, memory, or self-improvement drafts.

## Context
The repository no longer needs a bot-based operator surface. Keeping the old command and notification path creates unnecessary secret, security, documentation, and maintenance burden. The default operating model should be local Codex plus GitHub validation and local handoff artifacts.

## Constraints
- GitHub Actions must stay API-key-free.
- No external notification secrets may remain in tracked examples.
- Runtime commands should remain local and queue-safe.
- Historical files that only exist to describe the retired notification path may be deleted.

## Acceptance criteria
1. Runtime help no longer exposes bot or notification command flags.
2. Reporting renders local handoff artifacts and never attempts external notification dispatch.
3. Cron runner supports queue processing only.
4. Environment examples and docs no longer list retired notification variables or instructions.
5. Active tracked files no longer contain the retired notification keywords.
6. Validation and CI checks pass.

## Edge cases
- Old run records may still contain stale keys; the runtime should ignore them.
- Old local state under `codex_runtime_state/` is not migrated.
- A user passing old reporting modes should still get a local handoff rather than a network attempt.

## Platform target
codex-setting runtime and docs

## Delivery mode
existing repository + branch + PR

## Reporting mode
github_only

## Secret profile
No new secrets are required. The change removes retired notification secret placeholders from tracked configuration examples.

## Human handoff
- Review the removal diff for accidental loss of queue, handoff, GitHub delivery, or Product Factory behavior.
- If a future operator console is needed, design it through a new PRD with explicit approval and a fresh secret-boundary review.

## Validation commands
```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
python3 -m codex_runtime --prd PRD/2026-04-11-example-product-prd-web-ios.md --prepare-reporting --cwd . --pretty
CODEX_CRON_LOG_FILE=- CODEX_CRON_MODE=queue CODEX_CRON_MAX_RUNS=1 CODEX_CRON_MAX_IDLE_CYCLES=1 CODEX_CRON_POLL_SECONDS=0 ./scripts/cron-runner.sh
```

## Done when
- The retired notification surface is removed from runtime, docs, env examples, templates, and validation.
- GitHub-first local handoff, queue processing, readiness, and CI validation still pass.
