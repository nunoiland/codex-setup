# Plan: durable codex repo setup

## Source PRD

## Status
- Complete

## Platform target
- multi-platform

## Affected files or directories
- `AGENTS.md`
- `.codex/config.toml`
- `docs/PRD.md`
- `docs/TASK.md`
- `docs/BUSINESS_RULES.md`
- `docs/DESIGN.md`
- `docs/QA.md`
- `scripts/validate.sh`

## Tasks
1. Inspect the repo to confirm the runtime stack, package-manager situation, validation patterns, and current Codex conventions.
2. Replace the repository-level operating instructions with a shorter, durable `AGENTS.md` that still preserves PRD-first, approval, validation, and review gates.
3. Add concise docs-first templates for PRD, task framing, business rules, design notes, and QA expectations that fit this repo’s existing workflow.
4. Keep the repo-local Codex config aligned to the installed Codex CLI behavior and current safe-autonomy defaults, while preserving existing supported agent wiring.
5. Add a single validation entrypoint that uses only repo-native Python/stdlib and existing runtime checks.
6. Run the validation entrypoint plus repo diff checks, then summarize any residual approval boundaries.

## Risks and edge cases
- The current Codex CLI help is limited; avoid introducing config keys that are not already evidenced by the existing working repo config.
- This repo is Python stdlib-first and does not declare a package manager; validation should avoid adding dependencies.
- Keep approval boundaries explicit for auth, schema, payment, env, deploy, deletions, and irreversible actions.
- Do not weaken existing guard hooks while shortening instructions.

## Validation commands
```bash
./scripts/validate.sh
```

## Review gates
- QA review of doc clarity, validation coverage, and workflow regressions
- Security review of secret boundaries and approval guardrails
- Docs verification against current repo/runtime conventions

## Release and rollback notes
- Release note: this is a repo-setup/documentation hardening change only.
- Rollback by reverting the updated docs, AGENTS file, and validation script.
