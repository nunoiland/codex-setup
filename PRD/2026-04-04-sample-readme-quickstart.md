# Add Repository README Quickstart

## Goal

Add a top-level `README.md` that explains what this repository is for, how to use the PRD-driven Codex setup, and which files matter most.

## Scope

- Add a top-level `README.md`
- Explain the repository purpose
- Explain the PRD-driven workflow at a high level
- Point to the key files and directories users should read first

## Non-goals

- Changing agent behavior
- Changing hook behavior
- Adding dependencies
- Adding CI or automation

## Context

This repository currently contains project-scoped Codex configuration, agents, hooks, and skills, but it does not have a top-level README. A new user opening the repo has no immediate quickstart path.

## Constraints

- Keep the change documentation-only
- Match the existing PRD-driven philosophy of the repository
- Keep the README concise and practical

## Acceptance criteria

1. A new `README.md` exists at the repository root.
2. The README explains the purpose of the repository and the PRD-first workflow.
3. The README points to `AGENTS.md`, `.codex/config.toml`, `PRD/_template.md`, and `PLANS/README.md`.
4. The README includes a short "How to use" section.

## Edge cases

- The repository is configuration-only, not an application codebase.
- The README should not imply that the setup is global; it is project-scoped.
- The README should not claim validations or automation that do not exist.

## Platform target

repository/docs

## Validation commands

```bash
python3 -c 'from pathlib import Path; text = Path("README.md").read_text(); required = ["# codex-setting", "## What This Repo Is", "## How To Use", "AGENTS.md", ".codex/config.toml", "PRD/_template.md", "PLANS/README.md"]; missing = [item for item in required if item not in text]; assert not missing, missing'
git diff --check
```

## Done when

- `README.md` exists and satisfies the acceptance criteria
- Validation commands pass
- QA and security review are completed with no blocking issues
