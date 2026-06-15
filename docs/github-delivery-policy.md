# GitHub Delivery Policy

Use this policy for any PRD-driven product run that creates or updates code through GitHub.

## Goals

- Keep GitHub as the canonical record for code, validation history, and review state.
- Default to reviewable delivery, not silent protected-branch mutation.
- Make unattended runs safe enough for overnight execution and morning human QA.

## Default delivery mode

Unless a PRD explicitly says otherwise and a human has approved the change:

- use a branch, not a direct protected-branch push
- create a draft PR, not a ready-to-merge PR
- keep `main` and `master` protected from unattended pushes
- do not force-push

If your repository protects differently named branches such as `release`, `stable`, or `production`, set `CODEX_PROTECTED_BRANCHES` in the runtime environment so local guardrails match repository policy.

## Supported delivery modes

### 1. Existing repository + branch + draft PR

Preferred default.

Use when:
- the product already has a repository
- the run is modifying an existing codebase
- a human will QA and decide next steps in the morning

Expected output:
- branch created from the intended base branch
- commits pushed to the branch
- draft PR opened with validation notes and handoff summary

### 2. New repository + bootstrap branch + draft PR

Use when:
- the PRD explicitly requests a new repository
- repository-creation credentials are available from an approved external source
- the operator wants the run separated from an existing codebase

Expected output:
- repository created
- default branch initialized safely
- feature branch created for generated work when practical
- draft PR or equivalent reviewable handoff created if the platform and repo state allow it

### 3. Existing repository + branch + ready PR

Use only with explicit human approval in the PRD or live instruction.

Still required:
- validation results in the PR body or handoff
- no protected-branch direct push without approval

## Delivery rules

- Never assume direct push to `main` or `master` is acceptable.
- Never force-push unless a human explicitly approves it.
- Never create a repo or PR when required credentials are missing.
- If delivery partially succeeds, keep the successful GitHub artifacts and report the exact failure point.
- If one platform slice succeeds and another fails, preserve partial progress and report status by platform.

## Branch naming guidance

Prefer stable, reviewable names tied to the task:

- `codex/<short-slug>`
- `codex/prd-<short-slug>`
- `codex/<platform>-<short-slug>`

For multi-platform work, one branch is preferred unless the approved plan explicitly splits branches.

## PR requirements

Each draft PR should capture:

- source PRD
- platform target
- validation results
- known blockers or missing secrets
- QA checklist
- remaining manual work
- links to any morning handoff summary

The repository-level starting point for this is:

- [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md)

## Failure handling

If delivery fails:

- do not pretend the run is complete
- preserve local or branch progress when possible
- report whether the failure happened during repo creation, branch creation, commit, push, or PR creation
- report whether code generation itself succeeded before GitHub delivery failed

## Human approval boundaries

Human approval is still required for:

- direct protected-branch pushes
- force pushes
- auth-sensitive GitHub changes beyond the approved workflow
- release promotion from draft PR to merge or deployment

## API-key-free phase-1 GitHub Actions

The default repository automation is intentionally non-AI:

- `pr-validate` runs validation, whitespace checks, browser QA wrapper, and harness evidence collection.
- `nightly-harness` runs the same dry-run evidence path on a schedule.
- `automerge` only squash-merges same-repository PRs with the `automerge-approved` label after the configured required check passes.

This phase does not require `OPENAI_API_KEY` and does not use `openai/codex-action`.

For operator usage, follow:

- [`docs/how-to-use-codex-setting.md`](./how-to-use-codex-setting.md)

For the future API-key-based option, follow:

- [`docs/future-codex-action.md`](./future-codex-action.md)


## Current repository implementation note

Phase 2 now includes an opt-in local executor that can prepare branch, commit, push, and draft-PR commands. Actual execution stays gated behind `CODEX_ENABLE_LIVE_GITHUB=1` and explicit CLI invocation. Live remote success must still be validated against a non-production repository before calling the executor fully proven.

- The local executor assumes `git` and `gh` already have an authenticated path to GitHub, or that an approved PAT fallback is injected for `gh` use.
- GitHub App fields are still useful for readiness and policy, but they do not automatically log the local CLI into GitHub by themselves.
- For live validation against a non-default remote, set `CODEX_GITHUB_REMOTE` explicitly so push operations do not accidentally target the public `origin`.

For the recommended validation order before real use, follow:

- [`docs/live-validation-playbook.md`](./live-validation-playbook.md)
