# Git Quality and Security Tooling PRD

## Goal

Improve codex-setting's Git review, workflow validation, and local secret-prevention loop without adding API keys, SaaS secrets, mandatory local tools, or CI gitleaks enforcement.

## Summary

- Document Lazygit as an optional local review UI for staging and inspecting Codex-generated diffs.
- Add optional local `pre-commit` configuration.
- Add `gitleaks` only as a local pre-commit hook.
- Add GitHub Actions workflow linting through reviewdog/actionlint PR check annotations.
- Preserve API-key-free GitHub Actions and the existing GitHub-first validation model.

## Scope

- In scope:
  - `.pre-commit-config.yaml`
  - Git quality tooling docs and README/docs index links
  - PR validation workflow actionlint reviewdog step
  - validation guardrails confirming the new config stays optional and API-key-free
- Out of scope:
  - installing local developer tools
  - requiring `pre-commit`, `gitleaks`, or `lazygit` for normal repo validation
  - adding gitleaks CI enforcement
  - adding external SaaS keys, licenses, comments, or paid services

## Acceptance Criteria

1. Local operators can run `pre-commit install` and `pre-commit run --all-files`.
2. `gitleaks` runs only through local pre-commit configuration, not GitHub Actions.
3. PR validation includes actionlint output through reviewdog using GitHub check annotations.
4. GitHub Actions still require no `OPENAI_API_KEY`, gitleaks license, external SaaS secret, or local CLI installation.
5. `./scripts/validate.sh` verifies the expected config and fails if the optional-local boundary is weakened.

## Secret Profile

No new secrets are required. GitHub Actions may use the built-in `GITHUB_TOKEN` only. No gitleaks license, API key, webhook URL, provider key, or SaaS token is introduced.

## Validation Commands

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
```

Optional when local tools are installed:

```bash
pre-commit run --all-files
lazygit --version
```
