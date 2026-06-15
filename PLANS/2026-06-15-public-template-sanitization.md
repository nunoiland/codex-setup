# Plan: Public Template Sanitization

## Source PRD

- `PRD/2026-06-15-public-template-sanitization.md`

## Status

- Approved
- Current-tree sanitization completed
- Public history action pending human approval

## Tasks

1. Inspect current tree and commit history for public blockers.
2. Redact personal local paths from tracked docs.
3. Add `scripts/public-release-audit.py` for current-tree public readiness checks.
4. Add `docs/public-release-checklist.md` with the recommended public release flow.
5. Wire the current-tree audit into `./scripts/validate.sh`.
6. Run validation and report whether history cleanup still requires explicit approval.

## Affected files

- `PRD/2026-06-15-public-template-sanitization.md`
- `PLANS/2026-06-15-public-template-sanitization.md`
- `docs/public-release-checklist.md`
- `scripts/public-release-audit.py`
- `scripts/validate.sh`
- docs with personal absolute paths

## Risks

- Current Git history contains old extracted product and retired messenger commits; making the existing repository public without clean history would expose those commits.
- A current-tree audit cannot prove the entire Git history is safe.
- Gitleaks is not installed locally, so built-in regex checks are a fallback, not a replacement for a full secret scan.

## Validation commands

```bash
python3 scripts/public-release-audit.py
python3 scripts/product-workspace-audit.py
git diff --check
./scripts/validate.sh
./scripts/ci-pr-check.sh
```
