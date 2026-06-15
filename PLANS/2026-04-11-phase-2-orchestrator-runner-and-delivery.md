# Plan: Phase 2 orchestrator runner, delivery executor, and reporting transport

## Source PRD
- `<repo-root>/PRD/2026-04-11-phase-2-orchestrator-runner-and-delivery.md`

## Status
- In progress

## Platform target
- multi-platform

## PRD summary
- Goal: define and then implement the executable orchestration runner, GitHub delivery executor, and reporting transport foundation.
- Scope: runner model, runtime auth precedence, delivery executor, reporting transports, routing execution behavior, retries, and partial-success handling.
- Non-goals: autonomous deployment, live infrastructure mutation, committed secrets, self-evolving skill systems, and token-optimization work.

## Affected files or directories
- `<repo-root>/PRD/`
- `<repo-root>/PLANS/`
- `<repo-root>/docs/`
- `<repo-root>/.env.example`
- `<repo-root>/.github/`
- `<repo-root>/codex_runtime/`
- `<repo-root>/.agents/skills/`
- `<repo-root>/.codex/agents/`
- `<repo-root>/.codex/hooks/`
- `<repo-root>/README.md`
- `<repo-root>/AGENTS.md`

## Tasks
1. Define the executable run model.
   - Specify how a run is identified, queued, resumed, retried, or marked partial-success.
   - Define how a run maps PRD fields to platform slices and delivery expectations.
2. Define runtime auth and environment precedence.
   - Document GitHub App precedence over PAT fallback.
   - Document when a run should stop because reporting or provider credentials are missing.
3. Define the GitHub delivery executor contract.
   - Specify safe repository creation, branch creation, commit, push, and draft PR behavior.
   - Specify how failures are reported without overstating success.
4. Define reporting transport contracts.
   - Specify GitHub-first handoff generation.
   - Specify local handoff rendering boundaries and failure handling.
5. Add the minimum repository-side prompts, skills, templates, and docs needed to support implementation.
   - Prefer extending the existing repository conventions rather than adding broad new abstractions.
6. Validate the docs, config, and guardrails.
   - Validate TOML, hook syntax, diff hygiene, and any new docs or templates.
7. Run required review gates.
   - QA review
   - Security review
   - Release review only if rollout coordination becomes material

## Approval-required items
- Ask before implementing any real auth-sensitive runtime integration beyond placeholder contracts and docs.
- Ask before introducing new dependencies.
- Ask before adding any external command-and-control behavior.
- Ask before enabling repository creation, push, or PR creation through real credentials in this repository.

## Risks and edge cases
- Scope can balloon from “runner contract” into “full automation engine” too early.
- Auth precedence can become ambiguous if App and PAT paths are both present.
- Reporting transport logic can accidentally become source-of-truth logic if not kept secondary to GitHub.
- Retry logic can become dangerous without stable run identity and branch safety.
- Multi-platform status can become misleading if slices do not report separately.

## Validation commands
```bash
python3 - <<'PY'
from pathlib import Path
for rel in [
    'PRD/2026-04-11-phase-2-orchestrator-runner-and-delivery.md',
    'PLANS/2026-04-11-phase-2-orchestrator-runner-and-delivery.md',
]:
    text = Path(rel).read_text()
    assert text.strip(), rel
print('phase2-docs-ok')
PY
git diff --check
```

## Review gates
- QA review
- Security review
- Docs verification if auth or delivery assumptions change during implementation

## Release and rollback notes
- Release Phase 2 first as design and execution-boundary work, then implement actual runtime behavior in smaller increments.
- Roll back by reverting Phase 2 execution and delivery documents if the auth or execution boundary becomes unclear.
