# Plan: Product Workspace Boundary Hardening

## Source PRD

- `PRD/2026-06-14-product-workspace-boundary-hardening.md`

## Status

- Approved
- Completed

## Platform target

- repo tooling

## Affected files or directories

- `scripts/product-workspace-audit.py`
- `scripts/validate.sh`
- `docs/product-workspace-boundary.md`
- `README.md`
- `docs/README.md`

## Tasks

1. Add a Python audit script that scans top-level directories for product workspace markers.
2. Allow known `codex_set` template/runtime directories and ignored build/runtime folders.
3. Fail with a clear remediation message when a product-like top-level folder is found.
4. Wire the audit into `./scripts/validate.sh` and required-file checks.
5. Document the product repository boundary and link it from README/docs.

## Risks and edge cases

- False positives could block legitimate template directories, so the allowlist must include current repo directories.
- The guard should not inspect sibling product repositories outside `codex_set`.
- The guard should not require network, secrets, external CLIs, or provider credentials.

## Validation commands

```bash
python3 scripts/product-workspace-audit.py
./scripts/validate.sh
./scripts/ci-pr-check.sh
```

## Review gates

- QA: guard catches only product-like top-level workspaces.
- Security: no secrets or external service requirements are added.
- Release: validation remains API-key-free.

## Release and rollback notes

- Release as a normal settings repo hardening change.
- Rollback by removing the audit script, validation hook, and boundary doc link if the guard is too strict.
