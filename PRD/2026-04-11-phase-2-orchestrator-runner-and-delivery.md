# Phase 2: Add the Actual Orchestrator Runner, GitHub Delivery Executor, and Reporting Transport

## Goal

Upgrade `codex-setting` from a documented orchestration template into an executable orchestration foundation that can run approved PRD-driven workflows in controlled slices, manage GitHub delivery through a safe executor, and render morning handoff summaries while preserving GitHub as the canonical record.

## Scope

- In scope:
  - Define the executable runner model for queued or directly-invoked PRD-driven tasks.
  - Add a safe GitHub delivery executor design for repository creation, branch creation, commit, push, and draft PR handoff.
  - Add reporting transport design for GitHub-first handoff plus optional local handoff summaries.
  - Define runtime auth precedence and environment resolution for GitHub App, PAT fallback, and provider keys.
  - Define how platform routing is executed in work slices for `web`, `ios`, `android`, `api`, and supported combinations.
  - Define retry, partial-success, and blocker reporting behavior.
- In scope:
  - Add repository-side templates, prompts, skills, and execution docs needed to support a future implementation of this runner foundation.

## Non-goals

- Out of scope:
  - Fully autonomous production deployment.
  - Live DNS, domain, cloud, store, or production-infrastructure mutation without a human approval step.
  - Shipping real credentials, webhook URLs, or private keys in tracked files.
  - Building a self-evolving skill tree or autonomous skill synthesis engine in this phase.
  - Adding aggressive token-optimization infrastructure before the baseline runner is stable.

## Context

Phase 1 established the PRD-first contract, delivery policy, secret policy, handoff format, routing matrix, and workflow skills. The next step is to define the actual executable orchestration layer: how a run is represented, how platform slices are invoked, how GitHub delivery is performed safely, how reporting is rendered, and how failures are surfaced. This phase should keep the system aligned with the strengths observed in orchestration references such as `nrslib/takt` for structured workflow execution, `github/gh-aw` for controlled GitHub write behavior, and `openclaw/openclaw` for operator handoff reporting models, while staying conservative about auth-sensitive boundaries.

## Constraints

- Technical constraints:
  - The runner must remain PRD-driven and plan-first.
  - GitHub must remain the source of truth for code, branch, PR, and validation history.
  - Direct protected-branch pushes remain disallowed by default.
  - Runtime auth must prefer GitHub App flows and only fall back to PATs when explicitly allowed.
  - local handoff is the reporting transport in this phase, not an external command-and-control channel.
  - Secrets must be supplied through external runtime injection only.
- Product constraints:
  - The runner must support single-platform and multi-platform product PRDs without collapsing platform status into one opaque result.
  - Morning handoff output must preserve engineering status and draft business recommendations.
  - Human operators remain responsible for release approval, infrastructure setup, and final deployment decisions.
- Time or release constraints:
  - This phase should prioritize safe execution boundaries, observability, and deterministic handoff over feature breadth.
  - If implementation risk is high, the phase may end with a thin executable skeleton plus clear extension points rather than a fully feature-complete automation engine.

## Acceptance criteria

1. The repository defines a concrete runner model for executing PRD-backed tasks in ordered slices, including partial-success and retry semantics.
2. The repository defines a GitHub delivery executor model with explicit auth precedence, branch and draft PR defaults, and failure reporting.
3. The repository defines reporting transport behavior for GitHub-first local handoff rendering.
4. The repository makes runtime environment, secret boundaries, and approval-required auth-sensitive steps explicit enough to implement without guessing.
5. The repository changes for this phase remain narrowly scoped to orchestration, delivery, reporting, and runtime-boundary support.

## Edge cases

- The PRD is valid but required GitHub runtime credentials are unavailable.
- Repository creation succeeds but branch push or draft PR creation fails.
- One platform slice succeeds while another fails before delivery.
- GitHub delivery succeeds but local handoff reporting fails.
- Retry logic could duplicate handoffs or overwrite the wrong branch if run identity is ambiguous.
- A PAT is present but a GitHub App is also configured and precedence is unclear.
- A run is started without enough information to determine routing or base branch.
- Reporting is requested but local handoff rendering cannot write to the expected workspace.

## Platform target

- multi-platform

## Delivery mode

- existing repository + branch + draft PR by default
- new repository + controlled bootstrap only when the PRD and runtime auth allow it
- no direct push to protected branches without explicit human approval

## Reporting mode

- github_only by default
- github_only when runtime credentials are provided

## Secret profile

- Required secret: GitHub App credentials or approved fine-grained PAT
- Source of injection: external secret store or local runtime environment injection
- Owner or approver: repository operator
- Required secret: provider key for model-backed execution when needed
- Source of injection: external secret store or local runtime environment injection
- Owner or approver: operator

## Human handoff

- QA checks: confirm GitHub artifacts, platform status, validation output, and key product flows
- Manual release or infra tasks: environment setup, domain or DNS work, app signing, store submission, deployment approval
- Final approver: human operator

## Validation commands

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('PRD/2026-04-11-phase-2-orchestrator-runner-and-delivery.md').read_text()
required = [
    '# Phase 2: Add the Actual Orchestrator Runner, GitHub Delivery Executor, and Reporting Transport',
    '## Goal',
    '## Scope',
    '## Non-goals',
    '## Context',
    '## Constraints',
    '## Acceptance criteria',
    '## Edge cases',
    '## Platform target',
    '## Delivery mode',
    '## Reporting mode',
    '## Secret profile',
    '## Human handoff',
    '## Validation commands',
    '## Done when',
]
missing = [item for item in required if item not in text]
assert not missing, missing
print('phase2-prd-ok')
PY
git diff --check
```

## Done when

- A Phase 2 PRD exists that defines the executable runner, GitHub delivery executor, and reporting transport scope clearly.
- The PRD defines auth precedence, runtime boundaries, secret handling, and human approval boundaries clearly enough for a follow-on implementation plan.
- The PRD is specific enough that Phase 2 implementation can begin without guessing core runner or delivery behavior.
