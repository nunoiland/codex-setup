# Plan: Agent Army Routing Layer

## Source PRD

- `PRD/2026-06-06-agent-army-routing-layer.md`
- User-approved Agent Army Routing Layer 대량 이식 plan.

## Status

- Approved
- Complete

## Platform target

- multi-platform

## Affected files or directories

- `.codex/agents/`
- `codex_runtime/`
- `docs/`
- `README.md`
- `scripts/validate.sh`

## Tasks

1. Add PRD and plan records for the Agent Army routing layer.
2. Add docs for operating model, source review, service routing, team presets, and attribution boundary.
3. Add rewritten Codex-native specialist agents for product, design, engineering, QA/security/release, and growth/revenue.
4. Add runtime recommendation command:
   - `--recommend-agents`
   - `--service-type`
   - `--phase`
5. Update README/docs index and role-plugin docs so users know how to request agent teams.
6. Update validation guards for required docs, agents, runtime outputs, and workflow safety.

## Risks and edge cases

- Too many agents can create routing noise; the runtime must keep recommendations focused by service type and phase.
- External agent prompts must not be copied verbatim; docs must state rewritten-role and attribution boundaries.
- Heavy frameworks such as BMAD, MetaGPT, ChatDev, and agency-swarm must not become required default dependencies.
- Agents must not bypass PRD-first, plan-first, secret, auth, payment, deployment, or validation guardrails.

## Validation commands

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty
python3 -m codex_runtime --recommend-agents --service-type subscription_credit_saas --phase architecture --pretty
python3 -m codex_runtime --recommend-agents --service-type mobile_app --phase qa --pretty
python3 -m codex_runtime --recommend-agents --service-type finance_sensitive --phase release --pretty
```

## Review gates

- QA review confirms routing outputs are useful and deterministic.
- Security review confirms no new secrets, no live external framework requirement, and no workflow API-key dependency.
- Attribution review confirms external source links are cited and no external prompt bodies were copied.

## Release and rollback notes

- Release note: codex_set can now recommend service-specific agent teams through a local runtime command.
- Rollback: remove new docs, specialist agents, routing runtime module, CLI args, and validation guard additions.
