# Upgrade codex-setting into a PRD-Driven Product Orchestrator

## Goal

Turn this repository from a static Codex setup template into a PRD-driven orchestration template that can read a product PRD, route work by platform target, generate or update product code overnight, deliver the result to GitHub through controlled branch and draft PR workflows, and produce a morning handoff report with implementation status plus product, marketing, and revenue strategy drafts.

## Scope

- In scope:
  - Define the system behavior for reading a product PRD and extracting platform target, delivery mode, validation scope, and reporting preferences.
  - Add orchestration rules for platform-aware execution across web, iOS, Android, and supported combinations.
  - Define safe GitHub delivery behavior for repository creation or branch-based updates, commit, push, and draft PR creation.
  - Define secret-management rules so tokens, webhook URLs, and provider credentials are never stored in the repository.
  - Define morning handoff reporting for implementation status, validation results, QA checklist, and follow-up business strategy output.
  - Define optional reporting-channel support for local handoff while keeping GitHub as the system of record.
  - Update repository prompts, skills, guards, and templates needed to support the orchestrator workflow.

## Non-goals

- Out of scope:
  - Full autonomous production deployment without a human approval step.
  - Automatic domain purchase, DNS configuration, or live infrastructure cutover.
  - Storing secrets, API tokens, webhook URLs, or production credentials in tracked files.
  - Shipping a guarantee that all generated products are production-ready after a single unattended run.
  - Replacing GitHub as the canonical record for code, PRs, review state, and validation history.

## Context

This repository currently provides a PRD-first Codex template with project-scoped configuration, skills, hooks, and reviewer gates, but it does not yet define a full product-orchestration flow. The desired future state is a system that can accept a product PRD whose platform target may be `web`, `ios`, `android`, or a supported combination, run the appropriate builders overnight, publish work safely to GitHub, and produce a morning handoff report. Reference directions to consider during planning include orchestrated task execution, isolated workspaces, GitHub-safe delivery workflows, local handoff reporting, and reusable agent-skill ecosystems from repositories such as `nrslib/takt`, `github/gh-aw`, `openclaw/openclaw`, `NousResearch/hermes-agent`, `agency-agents-zh`, and related skill collections.

## Constraints

- Technical constraints:
  - The repository must remain PRD-driven and plan-first.
  - The system must interpret `platform target` from each product PRD instead of hard-coding a single platform.
  - GitHub delivery must default to branch plus draft PR rather than direct pushes to `main`.
  - Secrets must be injected from external secret stores, environment variables, GitHub App flows, or platform secret managers rather than committed files.
  - Reporting must render local handoff artifacts without external channel credentials.
  - Validation and review gates must remain explicit, with QA and security review required before work is considered complete.
- Product constraints:
  - The template should support product generation for web, iOS, Android, or selected combinations without requiring separate top-level repositories for each mode.
  - Morning handoff output should cover both engineering status and business follow-up suggestions such as marketing and revenue strategy drafts.
  - Human operators remain responsible for final QA, production environment setup, domain configuration, release approval, and deployment.
- Time or release constraints:
  - Initial rollout should prioritize safe orchestration and controlled delivery over maximum automation breadth.
  - The first version should prefer a minimal, extensible architecture that can later add richer memory, scheduling, or multi-channel control.

## Acceptance criteria

1. A product PRD can specify a platform target such as `web`, `ios`, `android`, `web+ios`, `web+android`, or `web+ios+android`, and the orchestration design clearly explains how routing should work for each supported mode.
2. The upgraded repository design defines a safe GitHub delivery model covering repository creation or existing-repository updates, branch creation, commit, push, and draft PR creation without requiring direct pushes to protected branches by default.
3. The repository documentation and workflow design define a clear secret-management policy for GitHub credentials, LLM provider keys, and any future external integrations.
4. The orchestrator design includes a morning handoff report format that summarizes implementation status, validation outcomes, QA follow-ups, unresolved risks, and product, marketing, or revenue strategy drafts.
5. The repository changes needed to support this workflow are narrow, explicit, and traceable to updated prompts, agents, skills, hooks, PRD templates, and planning guidance.

## Edge cases

- A product PRD omits or ambiguously states the platform target.
- A product PRD requests a platform combination that the current orchestrator version does not support.
- Repository creation succeeds but branch push or draft PR creation fails.
- Web succeeds while iOS or Android fails, requiring a partial-success handoff.
- Required secrets are missing, expired, mis-scoped, or unavailable at runtime.
- local handoff reporting fails even though GitHub delivery succeeds.
- Generated code passes some validations but fails build or integration checks.
- A product PRD asks for deployment, payment, auth, or infrastructure changes that exceed the approved automation boundary.

## Platform target

- multi-platform

## Validation commands

List the commands Codex should run after implementation.

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('PRD/2026-04-11-codex-setting-orchestrator-upgrade.md').read_text()
required = [
    '# Upgrade codex-setting into a PRD-Driven Product Orchestrator',
    '## Goal',
    '## Scope',
    '## Non-goals',
    '## Context',
    '## Constraints',
    '## Acceptance criteria',
    '## Edge cases',
    '## Platform target',
    '## Validation commands',
    '## Done when',
]
missing = [item for item in required if item not in text]
assert not missing, missing
PY
git diff --check
```

## Done when

Describe the exact completion bar.

- A system PRD exists for upgrading this repository into a PRD-driven product orchestrator.
- The PRD captures the intended orchestration behavior, GitHub delivery model, secret policy, reporting expectations, and review boundaries.
- The PRD is detailed enough to support a follow-on implementation plan in `PLANS/` without guessing core workflow assumptions.
