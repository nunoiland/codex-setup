# Public Release Checklist

Use this checklist before making this template available to everyone.

## Recommended release model

Do not make a long-running private working branch public directly.

Preferred options:

1. **New public template repo**: copy the sanitized current tree into a new repository with a clean first commit.
2. **Public-safe branch**: create an orphan branch from the sanitized current tree, push it, set that branch as the public/default branch, then make the repository public.

Both approaches keep private development history separate from the public template.

## Current-tree requirements

Run:

```bash
python3 scripts/public-release-audit.py
python3 scripts/product-workspace-audit.py
./scripts/validate.sh
./scripts/ci-pr-check.sh
```

The current tree should have:

- no real secrets, tokens, private keys, webhook URLs, or private endpoints
- no user-specific local absolute paths
- no extracted product workspaces or product-specific references
- no active retired messenger support references
- no required `OPENAI_API_KEY` in GitHub Actions
- no required external SaaS or paid service for normal validation

## History requirements

Before switching the repository to public visibility, verify the public branch history does not contain private work.

Recommended command examples:

```bash
git log --oneline --all --grep='product-specific-name' --regexp-ignore-case
git log --all --name-only --pretty=format: | sort -u | grep -Ei 'private-product|retired-messenger|local-user'
```

If old private work appears in history, do not publicize that branch. Use a clean public branch or a new public template repo.

## Do not expose

- product-specific PRDs or source code that moved to another repo
- local machine usernames or private folder paths
- provider keys, app secrets, tokens, or webhook URLs
- production domain settings, DNS API tokens, database URLs, or deploy credentials
- experimental runtime branches that are not part of the public template

## Safe public template contents

The public template may include:

- Codex configuration and local guardrails
- role agents and local skills
- PRD/PLAN templates and generic examples
- validation, harness, browser QA, and readiness scripts
- API-key-free GitHub Actions
- optional advanced contracts clearly marked as opt-in
- runnable web starter with placeholder-only env values
