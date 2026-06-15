# Plan: Add Repository README Quickstart

## Source PRD
- `PRD/2026-04-04-sample-readme-quickstart.md`

## Status
- Approved for test execution

## Platform target
- repository/docs

## Affected files or directories
- `README.md`

## Tasks
1. Read the PRD and confirm the change stays documentation-only.
2. Add a concise repository `README.md` that explains the purpose, workflow, and key files.
3. Run the PRD validation commands.
4. Perform QA and security review against the resulting diff.

## Risks and edge cases
- Overstating what the setup can do automatically
- Implying global Codex behavior instead of project-scoped behavior
- Missing key entry points for first-time users

## Validation commands
```bash
python3 -c 'from pathlib import Path; text = Path("README.md").read_text(); required = ["# codex-setting", "## What This Repo Is", "## How To Use", "AGENTS.md", ".codex/config.toml", "PRD/_template.md", "PLANS/README.md"]; missing = [item for item in required if item not in text]; assert not missing, missing'
git diff --check
```

## Review gates
- QA review
- Security review

## Release and rollback notes
- No release risk beyond documentation accuracy
- Rollback is deleting or reverting `README.md`
