# Trivy Security Scanning

Trivy is the template's first default CI security visibility layer for dependency vulnerabilities and configuration misconfigurations.

## Defaults

- PR validation runs Trivy in non-blocking mode.
- The scan target is the repository filesystem.
- Enabled scanners are `vuln,misconfig`.
- Severity is limited to `HIGH,CRITICAL`.
- Findings create evidence and a workflow summary, but do not block merge in phase 1.
- Secret scanning stays with local `gitleaks` pre-commit; Trivy secret scanning is not enabled in CI.
- GitHub Actions remain API-key-free and require no Trivy license or external SaaS secret.

## What Trivy checks here

The first-phase scan is meant to catch issues that matter for a fast product template:

- vulnerable Node/package dependencies detected from lockfiles
- risky Dockerfile and supported configuration files
- risky infrastructure-as-code style configuration if future product repos add it

The normal PR path does not build or scan a container image yet. Image scanning belongs in a later nightly or release workflow after the template's deployment path is finalized.

## Local usage

Install Trivy only on machines where you want local security checks:

```bash
brew install trivy
```

Run the same scanner scope used by PR validation:

```bash
trivy fs --scanners vuln,misconfig --severity HIGH,CRITICAL .
```

Treat findings as review input. Fix real vulnerable dependencies or unsafe config, but do not add broad ignores just to make the report quiet.

## CI behavior

PR validation writes a table report under the Actions evidence artifact path:

```text
codex_runtime_state/actions/security/trivy-pr-scan.txt
```

The workflow step uses `exit-code: "0"` and `continue-on-error: true` in phase 1. That means:

- vulnerability or misconfiguration findings do not fail the PR by themselves
- temporary Trivy setup or database download issues do not block normal validation
- reviewers still get evidence when the report is generated

## Future hardening path

Move gradually:

1. Keep non-blocking PR evidence until common findings are understood.
2. Add nightly Docker image scanning after release image naming is stable.
3. Consider blocking only `HIGH,CRITICAL` findings once false positives and ignore policy are reviewed.
4. Add SARIF upload only when the repo is ready to grant `security-events: write`.

## Boundaries

- Do not enable Trivy secret scanning in CI in this phase.
- Do not add `security-events: write` for Trivy in this phase.
- Do not require Docker image builds for normal PR validation.
- Do not commit `.trivyignore` or `.trivyignore.yaml` broad allowlists by default.
- Do not treat Trivy as a replacement for dependency updates, code review, auth review, or payment/security review.

## References

- [Trivy](https://github.com/aquasecurity/trivy)
- [Trivy Action](https://github.com/aquasecurity/trivy-action)
- [Trivy misconfiguration scanning](https://trivy.dev/docs/latest/scanner/misconfiguration/)
