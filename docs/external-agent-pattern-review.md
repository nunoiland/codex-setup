# External Agent Pattern Review

This document records which external patterns codex-setting adopts and which parts stay out of the default path.

## Reviewed sources

| Source | Useful pattern | Adoption decision |
| --- | --- | --- |
| `anthropics/knowledge-work-plugins` | Role-focused bundles with skills, commands, connectors, and sub-agents | Adopt the packaging model as local docs, agents, and skills. Do not add external connectors by default. |
| `Leonxlnx/taste-skill` | Brief-first design read, anti-generic UI rules, redesign-audit discipline | Adopt as taste review rules for product UI. Do not adopt randomization, mandatory GSAP, or visual dependency requirements. |
| `affaan-m/ECC` | Harness, verification loop, specialist routing, memory, security, and continuous-learning concepts | Adopt verification-loop and self-improvement contracts. Do not install ECC packages or replace existing runtime. |
| `Lum1104/Understand-Anything` | Optional codebase knowledge graph for onboarding, architecture review, and large repo navigation | Adopt as opt-in codebase cartography contract. Do not require graphs in CI. |
| `hardikpandya/stop-slop` | Direct prose review that removes AI tells, filler, formulaic structure, and vague copy | Adopt as copy-quality review for PRDs, docs, product copy, landing pages, and handoffs. |

## Default decision

The default path stays:

1. PRD first.
2. Plan before medium or large work.
3. Local Codex implementation.
4. GitHub Actions validation without AI provider keys.
5. Human review before adoption of self-improvement or optional external tools.

## What changes

- Add explicit reviewers for taste, copy, codebase mapping, and verification loops.
- Use the Agent Army routing layer for broader service-specific specialist assignment. See [`external-agent-army-source-review.md`](./external-agent-army-source-review.md).
- Add opt-in readiness output for external tools.
- Add runbooks so future installs happen through approval and review rather than ad hoc commands.

## What does not change

- No workflow requires `OPENAI_API_KEY`.
- No GitHub workflow requires plugin CLIs, knowledge graphs, ECC, Figma, Chromatic, Paperclip, Hermes, or Graphiti.
- No external code is executed by default.
- No external repository content becomes a hidden source of truth.

## Source links

- https://github.com/anthropics/knowledge-work-plugins
- https://github.com/Leonxlnx/taste-skill
- https://github.com/affaan-m/ECC
- https://github.com/Lum1104/Understand-Anything
- https://github.com/hardikpandya/stop-slop
