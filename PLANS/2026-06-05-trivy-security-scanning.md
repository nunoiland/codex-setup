# Plan: Trivy Security Scanning

## Source PRD

- `PRD/2026-06-05-trivy-security-scanning.md`
- User-approved Trivy introduction plan.

## Status

- Approved
- Complete

## Platform target

- multi-platform

## Affected files or directories

- `.github/workflows/pr-validate.yml`
- `scripts/validate.sh`
- `README.md`
- `docs/README.md`
- `docs/git-quality-tooling.md`
- `docs/security-scanning-trivy.md`

## Tasks

1. Add Trivy security scanning docs and connect them from README and the docs index.
2. Add a non-blocking PR workflow Trivy scan:
   - `aquasecurity/trivy-action@v0.36.0`
   - filesystem scan of `.`
   - scanners `vuln,misconfig`
   - severity `HIGH,CRITICAL`
   - `exit-code: "0"`
   - report output under the existing Actions evidence artifact path
3. Publish a short GitHub Actions summary pointing to the Trivy report.
4. Update validation guards to ensure Trivy stays API-key-free, non-blocking, and does not enable CI secret scanning.

## Risks and edge cases

- Trivy can produce false positives; first-phase findings are evidence, not merge blockers.
- Trivy DB download or remote action setup can fail; the first-phase scan remains non-blocking to avoid third-party scanner outages blocking product work.
- Secret scanning remains intentionally outside Trivy CI so the repo keeps the existing gitleaks local-only policy.
- Docker image scanning is deferred to future nightly or release hardening.

## Validation commands

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
```

Optional when local Trivy is installed:

```bash
trivy fs --scanners vuln,misconfig --severity HIGH,CRITICAL .
```

## Review gates

- QA review confirms Trivy report generation is visible as PR evidence.
- Security review confirms no new secrets, no SARIF permission, and no CI secret scanner.
- Docs review confirms local usage and first-phase non-blocking policy are clear.

## Release and rollback notes

- Release note: PR validation now creates non-blocking Trivy vulnerability and misconfiguration evidence.
- Rollback: remove the Trivy steps and validation guard additions if the action causes unacceptable CI instability.
