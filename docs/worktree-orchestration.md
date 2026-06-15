# Worktree-First Orchestration

This repository is designed for daily work in Git worktrees.

## Why worktree-first

Use worktrees to keep planning, implementation, and review isolated without losing local context.

Benefits:
- cleaner diffs per lane
- safer branch handling
- easier parallel platform work
- less context drift between planning and validation

## When to use one worktree vs several

### One worktree is enough
Use a single orchestrator worktree when the task is:
- small
- local to one platform or one document area
- unlikely to need parallel review or slice isolation

### Use several worktrees
Split into multiple worktrees when the task is:
- medium or large
- cross-platform
- risky enough to justify isolated review
- likely to create merge noise between lanes

## Default lane layout

### Small task
- `orchestrator` lane only
- branch shape: `codex/<slug>`

### Medium task
- `orchestrator` lane
- one implementation lane for the touched platform or slice
- optional `review` lane if the change is risky

### Cross-platform task
- `orchestrator` lane
- one implementation lane per platform or major slice
- one `review` lane before reintegration

## Branch naming

Use these defaults:
- orchestrator lane: `codex/<slug>`
- implementation lane: `codex/<slug>-<lane>`
- review lane: `codex/<slug>-review`

Examples:
- `codex/worktree-hardening`
- `codex/worktree-hardening-web`
- `codex/worktree-hardening-api`
- `codex/worktree-hardening-review`

Keep one branch per worktree.
Do not reuse the same branch name across multiple worktrees.
The init script refuses to create a lane if the branch already exists locally or on `origin`.

## Daily operating model

1. Start in the main checkout.
2. Read the PRD.
3. Write or update the plan.
4. Create the orchestrator worktree.
5. Add implementation worktrees only when the task benefits from isolation.
6. Reintegrate changes into the orchestrator lane.
7. Run validation from the orchestrator lane.
8. Use a review lane for large or risky changes.
9. Review and deliver from the orchestrator lane.

## Exact worktree creation commands

### Small task

```bash
./scripts/worktree-init.sh orchestrator my-task
```

### Medium task

```bash
./scripts/worktree-init.sh orchestrator my-task
./scripts/worktree-init.sh web my-task codex/my-task
```

Use `web` above as an example lane. Replace it with `ios`, `android`, `api`, or another scoped lane when needed.

### Cross-platform task

```bash
./scripts/worktree-init.sh orchestrator my-task
./scripts/worktree-init.sh web my-task codex/my-task
./scripts/worktree-init.sh api my-task codex/my-task
./scripts/worktree-init.sh review my-task codex/my-task
```

## Exact reintegration flow

Merge or rebase implementation lanes back into the orchestrator lane before PR delivery.

Example merge flow:

```bash
cd ../codex-setting-my-task

git merge --no-ff codex/my-task-web
git merge --no-ff codex/my-task-api
./scripts/validate.sh
```

Example review lane flow:

```bash
cd ../codex-setting-my-task-review
git merge --no-ff codex/my-task
./scripts/validate.sh
```

## Exact cleanup commands

Clean up an implementation lane after it has been reintegrated into the orchestrator branch:

```bash
./scripts/worktree-clean.sh ../codex-setting-my-task-web --merged-into codex/my-task --delete-branch
```

Clean up a review lane after it has been reintegrated into the orchestrator branch or `origin/main`:

```bash
./scripts/worktree-clean.sh ../codex-setting-my-task-review --merged-into codex/my-task --delete-branch
./scripts/worktree-clean.sh ../codex-setting-my-task --merged-into origin/main --delete-branch
```

Use `--force` only when you are intentionally discarding or bypassing the default safety checks.

## Isolation rules

- Keep planning and final integration in the orchestrator lane.
- Keep platform-specific edits inside their own implementation lane when practical.
- Avoid editing the same files in multiple worktrees.
- Rebase or merge lanes back into the orchestrator lane before opening or updating a PR.

## Reintegration rules

- Reintegrate implementation lanes into the orchestrator lane, not directly into protected branches.
- Re-run validation after reintegration.
- Use the review lane for large or risky diffs before final GitHub delivery.
- Final branch and PR creation should come from the orchestrator lane unless the approved plan says otherwise.

## Avoiding branch collisions and stale worktrees

- Use a clear slug per task.
- Do not recycle stale worktrees for unrelated tasks.
- Remove merged or abandoned worktrees promptly.
- If a lane becomes stale, rebase it onto the current orchestrator branch before continuing.
- If a branch name already exists locally or on `origin`, pick a new slug instead of reusing the old lane.

## Safe cleanup flow

Default cleanup is conservative:
- refuse to clean dirty worktrees unless `--force` is given
- refuse to remove protected branches by default
- refuse to delete unmerged branches unless `--force` is given
- allow `--merged-into <ref>` so cleanup can follow the real reintegration target
- prefer deleting the worktree first and the branch only when it is clearly safe
