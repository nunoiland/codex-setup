# PRD: Product Workspace Boundary Hardening

## Goal

Prevent product-specific workspaces from being accidentally tracked inside `codex_set` after a product has moved to its own repository.

## Scope

- Add a local validation guard for top-level product-like folders.
- Document the rule that `codex_set` is the settings/template OS, while real products should live in separate repositories or sibling worktrees.
- Keep the existing runnable web starter and operating stack unchanged.

## Non-goals

- Do not delete or move any external product repository.
- Do not add dependencies, services, secrets, migrations, auth, billing, or deployment changes.
- Do not block the built-in template source folders such as `src/`, `PRD/`, `PLANS/`, `docs/`, `scripts/`, or `.codex/`.

## Context

A product workspace can be created inside `codex_set` during early exploration. Once the product becomes its own repository, leaving the folder tracked in `codex_set` creates confusion, duplicate source-of-truth risk, and accidental deletion noise.

## Constraints

- The guard must be local and API-key-free.
- It must be deterministic and work in GitHub Actions.
- It must fail with a clear remediation message.

## Acceptance criteria

1. `./scripts/validate.sh` fails if a top-level product-like workspace is present in `codex_set`.
2. The guard allows normal template folders and ignored build/runtime folders.
3. Documentation explains when to keep work in `codex_set` versus a separate product repository.
4. Existing validation still passes on the clean settings repo.

## Platform target

- repo tooling

## Delivery mode

- existing repository + branch + commit

## Reporting mode

- github_only

## Secret profile

- Required secret: none
- Source of injection: none
- Owner or approver: human operator

## Human handoff

- QA checks: run validation and inspect any guard failure messages.
- Manual release or infra tasks: none.
- Final approver: repository owner.

## Validation commands

```bash
python3 scripts/product-workspace-audit.py
./scripts/validate.sh
./scripts/ci-pr-check.sh
```

## Done when

- Product-like folders are blocked from `codex_set` validation.
- The policy is linked from README and docs index.
- Validation passes.
