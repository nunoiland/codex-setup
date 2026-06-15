# Plan: Cron-first runtime setup

## Source PRD
- Operator request: prepare `codex-setting` before product work, starting with cron and then optimization.

## Status
- Complete

## Platform target
- local runtime / repository operations

## Affected files or directories
- `scripts/cron-runner.sh`
- `docs/cron-runner.md`
- `.codex/config.toml`
- `.codex/hooks.json`
- `docs/runner-contract.md`
- `README.md`
- `.env.example`
- `scripts/validate.sh`

## Tasks
1. Add a cron-safe one-shot wrapper that can drain the queue.
2. Keep live execution gated by the existing runtime environment flags.
3. Add operator documentation with safe crontab examples and failure handling.
4. Add placeholder cron settings to `.env.example` without storing secrets.
5. Update Codex project config and hook wiring for the installed Codex CLI schema.
6. Wire the cron wrapper into validation with an idle safe run.

## Risks and edge cases
- Cron does not inherit an interactive shell environment; operators must inject secrets externally.
- Duplicate cron invocations can overlap without a lock.
- Actual crontab installation is an operator action and should not be mutated automatically by this repository.
- Live builder, GitHub delivery, and reporting behavior must remain disabled unless existing explicit enable flags are set.

## Validation commands
```bash
./scripts/validate.sh
```

## Review gates
- QA review of cron docs and default behavior.
- Security review that no secrets are read from tracked files and live execution remains opt-in.

## Release and rollback notes
- Release by adding a crontab entry that calls `scripts/cron-runner.sh` from this repository.
- Roll back by removing the crontab entry; the repository wrapper is passive unless invoked.
