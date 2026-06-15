# Plan: GitHub README Finalization

## Source PRD

- `PRD/2026-06-15-github-readme-finalization.md`

## Status

- Approved
- Completed

## Tasks

1. Inspect current README, docs index, validation scripts, and repo status.
2. Rewrite README structure for GitHub readers while preserving bootstrap identity markers.
3. Keep claims concrete: included layers, commands, boundaries, and unsupported optional services.
4. Run anti-slop copy review manually against the updated README.
5. Run validation and QA checks.
6. Summarize remaining risks and whether the repo is ready to commit.

## Affected files

- `README.md`
- `scripts/validate.sh`
- `PRD/2026-06-15-github-readme-finalization.md`
- `PLANS/2026-06-15-github-readme-finalization.md`

## Risks

- Overstating optional Hermes/Paperclip/Graphiti capabilities as installed runtime.
- Accidentally changing bootstrap markers used by `scripts/bootstrap-template.py`.
- Making README too long for GitHub scanning.

## Validation commands

```bash
git diff --check
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
```
