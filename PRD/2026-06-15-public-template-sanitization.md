# PRD: Public Template Sanitization

## Goal

Prepare `codex_set` to become a public, reusable Codex product template without exposing product-specific work, personal local paths, retired messenger features, or real secrets.

## Scope

- Document the public-release policy and recommended history-cleaning approach.
- Add a current-tree public-release audit for obvious public blockers.
- Sanitize tracked docs that contain personal absolute paths.
- Keep optional advanced capabilities documented as opt-in, not enabled by default.
- Do not rewrite Git history or change repository visibility without a separate explicit approval.

## Non-goals

- Do not delete files in this step.
- Do not force-push or rewrite existing branches in this step.
- Do not change GitHub repository visibility in this step.
- Do not add dependencies or external services.
- Do not remove useful public template capabilities such as agents, skills, validation, harness, or Product Factory contracts.

## Public safety requirements

- No real secrets, tokens, private keys, passwords, webhook URLs, or private endpoints in tracked files.
- No user-specific absolute local paths such as `/Users/<real-user>/...`.
- No product-specific folders or references from extracted products.
- No active retired messenger support references.
- History must be cleaned before public visibility because previous commits contain removed product and messenger work.

## Recommended history approach

Use a public-safe orphan branch or a new sanitized public repository instead of force-rewriting the private working branch.

Preferred path:

1. Keep this private working branch as internal history.
2. Create a clean public branch from the current sanitized tree with one initial commit.
3. Push that branch to GitHub.
4. Set it as the public/default branch only after final scan.
5. Then make the repository public or create a new public template repo from that branch.

## Secret profile

- Required secret: none
- Source of injection: none
- Owner or approver: repository owner

## Validation commands

```bash
python3 scripts/public-release-audit.py
python3 scripts/product-workspace-audit.py
git diff --check
./scripts/validate.sh
./scripts/ci-pr-check.sh
```
