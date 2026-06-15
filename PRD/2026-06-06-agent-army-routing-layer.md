# Agent Army Routing Layer PRD

## Goal

Turn codex_set into a product template that can recommend a service-specific Codex-native agent team for discovery, PRD, UX, architecture, implementation, QA, release, and growth work.

## Summary

- Add a broad local Agent Army inspired by external agent catalogs and BMAD-style workflows.
- Keep all roles rewritten for this repository instead of copying external prompt files.
- Add a runtime recommendation command that maps service type plus lifecycle phase to primary, reviewer, and optional agents.
- Preserve API-key-free GitHub Actions and keep heavy external frameworks out of the default path.

## Scope

- In scope:
  - PRD, plan, and docs for the Agent Army operating model
  - additional `.codex/agents/*.toml` specialists
  - runtime agent routing command
  - validation guards for docs, agents, routing outputs, and workflow safety
- Out of scope:
  - installing BMAD, agency-swarm, MetaGPT, ChatDev, or external CLIs
  - copying external repo prompt files verbatim
  - changing model provider secrets, deployment, auth, payment, or GitHub Action secret requirements
  - autonomous production operation by any agent

## External Pattern Inputs

The implementation uses these sources as pattern references only:

- `msitarzewski/agency-agents`: broad role taxonomy across engineering, design, product, growth, sales, and security.
- `bmad-code-org/BMAD-METHOD` and `xmm/codex-bmad-skills`: phase-based product delivery from discovery through QA.
- `wshobson/agents`: plugin/agent/skill marketplace structure and cross-harness routing ideas.
- `NicholasSpisak/claude-code-subagents`: keyword and domain-based agent decision matrix.
- `FoundationAgents/MetaGPT`, `OpenBMB/ChatDev`, and `VRSEN/agency-swarm`: software-company and communication-flow concepts, kept as reference-only because they are heavier runtime frameworks.
- `rahulvrane/awesome-claude-agents` and `PabloLION/bmad-plugin`: discovery and plugin packaging references.

## Acceptance Criteria

1. New docs explain the Agent Army operating model, source review, routing matrix, team presets, and attribution boundary.
2. The repo includes a broad set of rewritten Codex-native specialist agents for product, design, engineering, QA, security, release, growth, and revenue work.
3. `python3 -m codex_runtime --recommend-agents --service-type <type> --phase <phase> --pretty` returns primary, reviewer, optional agents, validation gates, and risks.
4. Supported service types include web SaaS, subscription/credit SaaS, marketplace, mobile app, AI agent service, data dashboard, finance-sensitive, and consumer content app.
5. Supported phases include discovery, PRD, UX, architecture, implementation, QA, release, and growth.
6. Validation confirms required docs/agents exist and that GitHub Actions do not require external agent frameworks or API keys.

## Secret Profile

No new secrets are required. External frameworks and provider-backed runtimes remain off the default path. Any future live multi-agent runtime must use externally injected credentials and a separately approved plan.

## Validation Commands

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty
python3 -m codex_runtime --recommend-agents --service-type subscription_credit_saas --phase architecture --pretty
python3 -m codex_runtime --recommend-agents --service-type mobile_app --phase qa --pretty
python3 -m codex_runtime --recommend-agents --service-type finance_sensitive --phase release --pretty
```
