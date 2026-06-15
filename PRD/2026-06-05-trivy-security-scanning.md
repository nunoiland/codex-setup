# Trivy Security Scanning PRD

## Goal

Add Trivy as a default, API-key-free security visibility layer for the codex_set product template without turning first-phase findings into merge blockers.

## Summary

- Add non-blocking Trivy filesystem scanning to PR validation.
- Scan for dependency vulnerabilities and configuration misconfigurations.
- Keep secret scanning in the existing local gitleaks pre-commit boundary.
- Preserve API-key-free GitHub Actions and avoid new SaaS secrets, licenses, or provider credentials.

## Scope

- In scope:
  - PR validation workflow Trivy scan
  - Trivy security scanning docs and README/docs index links
  - validation guards confirming the non-blocking and no-secret-scanner policy
- Out of scope:
  - Docker image scanning in the normal PR path
  - SARIF upload to GitHub Security tab
  - `security-events: write` workflow permissions
  - Trivy secret scanning in CI
  - blocking PRs on findings in the first phase

## Acceptance Criteria

1. PR validation runs `aquasecurity/trivy-action@v0.36.0` in filesystem mode.
2. The scan uses `scanners: vuln,misconfig`, `severity: HIGH,CRITICAL`, and `exit-code: "0"`.
3. The scan writes a table report to the existing Actions evidence artifact path.
4. The workflow summary points reviewers to the Trivy report when present.
5. GitHub Actions require no `OPENAI_API_KEY`, Trivy license, external SaaS secret, or SARIF permission.
6. `./scripts/validate.sh` fails if the workflow enables Trivy secret scanning or turns the first-phase scan into a blocking gate.

## Secret Profile

No new secrets are required. GitHub Actions may use only the built-in `GITHUB_TOKEN` already used by workflow annotation tooling. Trivy secret scanning is not enabled in CI; local secret checks remain handled by gitleaks pre-commit.

## Validation Commands

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
```

Optional when Trivy is installed locally:

```bash
trivy fs --scanners vuln,misconfig --severity HIGH,CRITICAL .
```
