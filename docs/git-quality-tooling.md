# Git Quality Tooling

Use these tools to review Codex-generated changes quickly and catch common Git, workflow, and secret mistakes before merge.

## Defaults

- Lazygit is optional local UI tooling. It is never required in CI.
- `pre-commit` is optional local commit-time validation. It is not required by `./scripts/validate.sh`.
- `gitleaks` runs through local pre-commit only in this phase. GitHub Actions do not require a gitleaks license or secret.
- `reviewdog/action-actionlint` runs in PR validation and reports GitHub Actions workflow issues as check annotations.
- Trivy runs in PR validation as non-blocking vulnerability and misconfiguration evidence. It does not run secret scanning in CI.
- GitHub Actions remain API-key-free.

## Local setup

Install optional tools only on machines where you want the local workflow.

```bash
# Optional Git UI for reviewing and staging Codex diffs.
brew install lazygit

# Optional local pre-commit manager.
pip install pre-commit

# Install repository hooks.
pre-commit install
```

Run the full local hook set when adding or changing hook config:

```bash
pre-commit run --all-files
```

Use Lazygit for human review:

```bash
lazygit
```

Recommended Lazygit flow:

1. Review unstaged Codex changes.
2. Stage only the intended files or hunks.
3. Keep unrelated local state unstaged.
4. Commit only after `./scripts/validate.sh` passes.
5. Push the branch and let GitHub Actions produce PR evidence.

## What pre-commit checks

The local hook config checks:

- YAML, TOML, and JSON parseability
- trailing whitespace
- final newline consistency
- merge conflict markers
- accidentally large added files
- possible secrets through `gitleaks`

Do not bypass `gitleaks` unless the finding is verified as a false positive. If a real secret is found, rotate it before continuing.

## CI behavior

PR validation runs `reviewdog/action-actionlint` with:

- reporter: `github-pr-check`
- failure threshold: `error`
- no PR review comment mode
- no extra secrets beyond GitHub's built-in `GITHUB_TOKEN`

This catches workflow syntax, expression, shell, and common security mistakes before merge without requiring AI/API credentials.

PR validation also runs Trivy in non-blocking mode for:

- dependency vulnerability evidence
- Dockerfile and supported config/IaC misconfiguration evidence

See [`security-scanning-trivy.md`](./security-scanning-trivy.md) for the scanner boundary and local usage.

## Boundaries

- Do not add gitleaks CI enforcement without a new approval.
- Do not enable Trivy secret scanning in CI in this phase.
- Do not add `pre-commit/action` as a required PR check in this phase.
- Do not add `.gitleaksignore` broad allowlists by default.
- Do not require local tool installation for normal repository validation.

## References

- [pre-commit](https://pre-commit.com/)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [actionlint](https://github.com/rhysd/actionlint)
- [reviewdog/action-actionlint](https://github.com/reviewdog/action-actionlint)
- [Trivy](https://github.com/aquasecurity/trivy)
- [lazygit getting started](https://lazygit.dev/docs/getting-started/)
