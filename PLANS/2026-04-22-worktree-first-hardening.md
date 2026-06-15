# Plan: worktree-first hardening

## Source PRD
- `PRD/2026-04-11-codex-setting-orchestrator-upgrade.md`

## Status
- Complete

## Platform target
- multi-platform

## Affected files or directories
- `AGENTS.md`
- `README.md`
- `.codex/config.toml`
- `.codex/instructions.md`
- `.codex/hooks/guard.py`
- `.codex/agents/*.toml`
- `docs/worktree-orchestration.md`
- selected `docs/*.md` default-path docs
- `scripts/validate.sh`
- `scripts/worktree-init.sh`
- `scripts/worktree-clean.sh`

## Tasks
1. Keep the repository PRD-first and plan-first while splitting durable repo rules from short model instructions.
2. Verify `.codex/config.toml` keys against the installed Codex client and trim the configured agent surface to the smallest daily-use set.
3. Harden hook guardrails for worktree-first daily use, destructive git protection, force-push protection, and risky remote mutations.
4. Add minimal worktree setup and cleanup scripts with safe branch naming and cleanup rules.
5. Add one repo-wide validation entrypoint for docs/config/runtime/script integrity.
6. Update README and default-path docs so GitHub plus the local repo stay canonical and local handoff becomes optional/advanced, not default.
7. Keep runtime code intact unless a default-path mismatch requires a narrow change.

## Risks and edge cases
- The installed Codex client exposes config support indirectly; remove or avoid any key that cannot be substantiated from the local client.
- local handoff support exists in runtime code and docs; demote it from the default path without breaking optional advanced usage.
- File deletion requires approval; avoid deleting speculative agent files and instead demote them by removing them from the active config surface.
- Worktree cleanup must avoid deleting dirty worktrees or protected branches by default.

## Validation commands
```bash
./scripts/validate.sh
python3 -m py_compile .codex/hooks/guard.py codex_runtime/*.py
codex --help
codex features list
git diff --check
```

## Review gates
- QA review for workflow clarity, validation coverage, and daily-use ergonomics
- Security review for secret hygiene, protected-branch safety, and risky command guardrails
- Docs verification against current runtime and Codex client behavior

## Release and rollback notes
- Release note: default workflow becomes worktree-first, GitHub-first, and local handoff-optional.
- Roll back by reverting the focused docs/config/hook/script changes in this plan.
