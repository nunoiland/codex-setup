# External Tools Opt-in Runbook

Use this runbook before installing or enabling any external tool inspired by the reviewed repositories.

## Default

External tool mode is off:

```bash
CODEX_EXTERNAL_TOOLS_MODE=off
```

Normal validation and GitHub Actions must work in this mode.

## Opt-in check

Before enabling a tool, answer:

1. What problem does the tool solve that local inspection cannot solve cheaply?
2. Does it require network access, API keys, secrets, or external accounts?
3. Does it write generated artifacts into the repo?
4. How will the output be reviewed by a human?
5. How will we remove it if it becomes noisy or stale?

## Approved opt-in categories

- local knowledge graph for large codebase onboarding
- local verification harness for repeated failures
- local design or copy review checklists
- local role plugin experiments that use markdown-only skills

## Not approved by default

- provider-backed AI jobs in GitHub Actions
- external plugin connectors with broad data access
- automatic self-improvement commits
- automatic dependency installation
- automatic production deploys
- tools that require secrets in tracked files

## Readiness commands

```bash
python3 -m codex_runtime --operator-readiness --pretty
CODEX_EXTERNAL_TOOLS_MODE=opt-in python3 -m codex_runtime --operator-readiness --pretty
CODEX_EXTERNAL_TOOLS_MODE=opt-in CODEX_UNDERSTAND_ANYTHING_MODE=local python3 -m codex_runtime --operator-readiness --pretty
```

## Adoption path

1. Keep the tool disabled.
2. Add a PRD explaining the need and risk.
3. Add or update a plan.
4. Install or run the tool locally after approval.
5. Commit only reviewed, sanitized artifacts.
6. Keep GitHub Actions independent unless a separate PRD approves otherwise.
