# Product Workspace Boundary

`codex_set` is the settings/template OS. It should not become the long-term home for individual product repositories.

## Default rule

Use `codex_set` for:

- shared Codex settings
- agents and skills
- validation scripts
- Product Factory contracts
- template starter code
- PRD/PLAN examples for improving the template itself

Use a separate product repository or sibling worktree for:

- real product Android, iOS, web, or backend code
- product-specific secrets and environment setup
- product-specific GitHub remotes
- app store, deployment, or customer-facing release work
- ongoing product PRDs and plans after bootstrap

## Safe product creation flow

1. Use `codex_set` to inspect the PRD and choose agents.
2. Create the product repo outside `codex_set`, for example `<workspace-parent>/<product-slug>`.
3. Copy or bootstrap only the needed template pieces.
4. Keep product commits, branches, and remotes in the product repo.
5. Return to `codex_set` only for settings, agents, validation, and template improvements.

## Validation guard

`./scripts/validate.sh` runs `scripts/product-workspace-audit.py`.

The guard fails when it finds a top-level directory that looks like a product workspace, such as a folder with:

- its own `.git`
- `PRD/` plus `PLANS/`
- `android/`, `ios/`, `server/`, or product `app/` markers with product docs

If this fails, move the product folder outside `codex_set` or intentionally convert it into a separate repository before committing.

## Why this matters

This prevents:

- duplicate source-of-truth between `codex_set` and a product repo
- accidental product deletion commits in `codex_set`
- product secrets or generated artifacts entering the settings repo
- validation noise from product-specific toolchains
