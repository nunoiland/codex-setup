# Role Plugin Operating Model

Codex-setting uses role bundles as a local operating pattern, not as a required external plugin runtime.

## Purpose

A role bundle groups the context needed for a job:

- agent definition for the reviewer or specialist
- skill instructions for repeatable workflow
- docs contract for acceptance criteria
- optional runbook for tools that need approval

## Current local roles

Core roles:

- orchestrator
- platform builders
- QA reviewer
- security reviewer
- senior product designer
- docs researcher

External-pattern roles added by this layer:

- copy quality reviewer
- codebase cartographer
- verification loop specialist

Agent Army roles added by the service routing layer:

- product and business specialists
- design and UX specialists
- engineering specialists
- QA, security, compliance, release, and observability specialists
- growth, revenue, sales, and customer success specialists

Use [`agent-army-operating-model.md`](./agent-army-operating-model.md) and [`service-agent-routing-matrix.md`](./service-agent-routing-matrix.md) to route these roles by service type and phase.

## Rules

- Use local roles before adding external connectors.
- Keep each role narrow enough to give concrete findings.
- Prefer role output that names affected files, user impact, and smallest fix.
- Treat role output as review input, not automatic permission to merge or deploy.
- Keep skills markdown-only and dependency-free unless a PRD approves otherwise.

## Command pattern

This repository does not add slash commands in this phase. Instead, use natural prompts:

```text
Use copy_quality_reviewer to review this PRD and README for AI-sounding prose.
Use codebase_cartographer to map this new product repo before implementation.
Use verification_loop_specialist to turn this failing check into reproduction steps and regression candidates.
Run python3 -m codex_runtime --recommend-agents --service-type web_saas --phase architecture --pretty, then use the recommended primary and reviewer agents.
```

## Future extension

If a future tool supports local command files, commands may mirror the existing skill names. They must still obey PRD-first, plan-first, secret-boundary, and validation rules.
