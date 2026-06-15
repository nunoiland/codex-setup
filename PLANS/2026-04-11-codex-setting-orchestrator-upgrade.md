# Plan: Upgrade codex-setting into a PRD-driven product orchestrator

## Source PRD
- `<repo-root>/PRD/2026-04-11-codex-setting-orchestrator-upgrade.md`

## Status
- In progress

## Platform target
- multi-platform

## PRD summary
- Goal: upgrade the repository so it can interpret product PRDs, route work by platform target, deliver safely to GitHub, manage secrets outside the repo, and produce a morning handoff report with engineering and business outputs.
- Scope: platform routing, GitHub delivery workflow, secret policy, reporting channels, repository prompts/skills/hooks/templates.
- Non-goals: autonomous production deployment, live domain or infrastructure cutover, committed secrets, and bypassing GitHub as the canonical record.

## Affected files or directories
- `<repo-root>/AGENTS.md`
- `<repo-root>/README.md`
- `<repo-root>/.env.example`
- `<repo-root>/PRD/_template.md`
- `<repo-root>/PRD/`
- `<repo-root>/PLANS/`
- `<repo-root>/docs/`
- `<repo-root>/.github/`
- `<repo-root>/.codex/config.toml`
- `<repo-root>/.codex/hooks.json`
- `<repo-root>/.codex/hooks/guard.py`
- `<repo-root>/.codex/agents/`
- `<repo-root>/.agents/skills/`

## Tasks
1. Refine repository-level PRD and template support.
   - Extend `<repo-root>/PRD/_template.md` so product PRDs can declare platform target combinations, delivery mode, reporting mode, and secret profile expectations.
   - Add example guidance that distinguishes product PRDs from system PRDs.
2. Update the repository operating contract and top-level docs.
   - Expand `<repo-root>/AGENTS.md` and `<repo-root>/README.md` to describe the orchestrator boundary, GitHub-as-source-of-truth, branch-plus-draft-PR default, and manual release responsibilities.
3. Add minimal orchestration skills and agent guidance.
   - Reuse the current PRD-first architecture where possible.
   - Add or update only the smallest set of agent configs and skills needed for platform routing, GitHub delivery, reporting, and strategy-output generation.
   - Prefer extending `prd_orchestrator`, existing builders, and review roles before introducing many new abstractions.
4. Tighten hooks and guardrails.
   - Update `<repo-root>/.codex/hooks/guard.py` and hook wiring so the repo blocks unsafe patterns such as direct protected-branch pushes, missing PRD platform target, and obvious secret leakage in diffs.
   - Keep approval gates explicit for dependencies, auth changes, payment work, migrations, and destructive operations.
5. Define GitHub delivery and reporting workflow docs.
   - Document the supported delivery modes: new repo creation, existing repo branch creation, commit/push, and draft PR handoff.
   - Document optional local handoff reporting as a secondary notification channel.
   - Document required external secret sources and least-privilege guidance.
6. Add planning and usage examples.
   - Add at least one example system PRD and one example product PRD shape that exercises `web`, `ios`, `android`, and combination routing.
   - Update planning guidance if new execution stages or review gates are introduced.
7. Validate the repository changes.
   - Run the validation commands defined in the updated PRD and any repository-relevant checks for changed Python or JSON/TOML files.
8. Run required review gates before completion.
   - QA review
   - Security review
   - Release review only if rollout coordination becomes material

## Approval-required items
- Ask before adding any new dependencies.
- Ask before introducing any auth-sensitive integration beyond documentation and prompt wiring, including GitHub App setup details or external command channels.
- Ask before adding any file deletions or migration-like behavior.

## Risks and edge cases
- Scope can balloon if the first pass tries to implement execution scheduling, chat control, GitHub automation, and business-strategy generation all at once.
- Secret policy can become inconsistent if reporting channels are documented without a unified credential model.
- Platform routing can drift from the PRD if template fields are underspecified.
- GitHub delivery safeguards must not accidentally block normal local repository work.
- Optional chat channels should not become the primary record of work status; GitHub must remain canonical.
- Business-strategy outputs should be framed as drafts to avoid overstating confidence.

## Validation commands
```bash
python3 - <<'PY'
from pathlib import Path
for rel in [
    'PRD/2026-04-11-codex-setting-orchestrator-upgrade.md',
    'PLANS/2026-04-11-codex-setting-orchestrator-upgrade.md',
]:
    text = Path(rel).read_text()
    assert text.strip(), rel
print('docs-ok')
PY
git diff --check
python3 - <<'PY'
import py_compile
py_compile.compile('.codex/hooks/guard.py', cfile='/tmp/codex-setting-guard.pyc', doraise=True)
print('pycompile-ok')
PY
```

## Review gates
- QA review
- Security review
- Docs verification if workflow assumptions change during implementation

## Release and rollback notes
- Release as repository-template documentation and workflow changes first, not as unattended production automation.
- Roll back by reverting the orchestrator-related prompt, skill, hook, and template changes if the new workflow proves too broad or noisy.
