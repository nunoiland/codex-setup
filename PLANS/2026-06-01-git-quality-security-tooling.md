# Plan: Git Quality and Security Tooling

## Source

- `PRD/2026-06-01-git-quality-security-tooling.md`
- User-approved plan for Lazygit, pre-commit, gitleaks, actionlint, and reviewdog integration.

## Implementation

1. Add `.pre-commit-config.yaml` with safe local-only hooks:
   - `pre-commit/pre-commit-hooks@v6.0.0`
   - `gitleaks/gitleaks@v8.24.2`
2. Update PR validation workflow:
   - add `checks: write`
   - add `reviewdog/action-actionlint@v1.72.0`
   - use `reporter: github-pr-check`
   - use `fail_level: error`
3. Add `docs/git-quality-tooling.md` with local setup and usage guidance:
   - Lazygit is optional
   - pre-commit is optional local setup
   - gitleaks is local pre-commit only
   - reviewdog/actionlint is CI PR check annotation only
4. Update README and docs index to link the new guide.
5. Update `scripts/validate.sh` to guard:
   - required config/docs exist
   - expected pre-commit hooks are present
   - reviewdog/actionlint workflow config is present
   - workflows still do not require API keys, gitleaks license, or external service secrets

## Validation

Run:

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
```

If installed locally, also run:

```bash
pre-commit run --all-files
lazygit --version
```

## Risks

- The first local `pre-commit run --all-files` may download hook environments and take time.
- `gitleaks` false positives should be reviewed carefully; do not add broad allowlists by default.
- reviewdog annotations depend on GitHub Actions permissions; keep `checks: write` scoped to PR validation only.
