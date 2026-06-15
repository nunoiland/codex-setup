# Plan: Codex external pattern optimization

## Source PRD
- `PRD/2026-05-28-codex-external-pattern-optimization.md`

## Status
- Approved for implementation

## Platform target
- codex-setting runtime and docs

## Summary
Add an aggressive but safe opt-in layer that captures useful patterns from external agent, plugin, harness, knowledge graph, design taste, and copy-quality projects while keeping default GitHub Actions and local validation dependency-free.

## Affected files or directories
- `PRD/`, `PLANS/`, `docs/`, `.codex/agents/`, `.agents/skills/`
- `codex_runtime/operator_readiness.py`
- `.env.example`, `README.md`, `scripts/validate.sh`

## Implementation tasks
1. Add the PRD and this plan.
2. Add pattern review and operating contracts for role plugins, knowledge graphs, taste/copy review, verification loops, and opt-in external tools.
3. Add specialist agents for copy quality, codebase cartography, and verification loops.
4. Add local skills for anti-slop copy review, frontend taste review, codebase understanding, and verification-loop review.
5. Extend operator readiness and env docs with opt-in external tool modes.
6. Update README, docs index, and validation requirements so the layer is discoverable and guarded.
7. Run validation and optional-readiness checks.

## Guardrails
- No external dependencies or services are installed in this slice.
- No provider keys, plugin secrets, SaaS tokens, webhook URLs, or private endpoints are added.
- GitHub Actions remain API-key-free.
- External source content is summarized with attribution; do not copy large skill bodies or repo content.
- Missing optional tools warn in readiness and never create blockers for normal PR validation.

## Validation commands
```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
CODEX_EXTERNAL_TOOLS_MODE=opt-in CODEX_UNDERSTAND_ANYTHING_MODE=local CODEX_VERIFICATION_LOOP_MODE=local python3 -m codex_runtime --operator-readiness --pretty
```

## Review gates
- QA review for validation and discoverability.
- Security review for secrets, dependency, external tool, and workflow boundaries.
- Copy quality review for README/docs tone where user-facing instructions changed.

## Risks and edge cases
- Too many optional tools can confuse daily workflow, so docs must keep local Codex plus GitHub validation as the default.
- Knowledge graph generation can be costly for large repos, so it must stay opt-in and local.
- Taste and copy rules can become subjective, so reviewers must return concrete findings tied to screens, docs, or user outcomes.
- Verification loops can become busywork, so the default should focus on reproduction command, evidence, regression candidate, and next fix.

## Release and rollback notes
- Rollback is file-level revert of the new docs, agents, skills, env entries, and readiness output.
- No runtime migrations, dependencies, or external service state are introduced.
