# External Agent Army Source Review

This review records which external patterns are useful for codex_set and what is intentionally not adopted.

## Source summary

| Source | Useful pattern | Adopted boundary |
| --- | --- | --- |
| [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) | Broad role taxonomy across engineering, design, product, growth, sales, support, and security | Rewritten local role names and responsibilities only; no prompt body copying |
| [`bmad-code-org/BMAD-METHOD`](https://github.com/bmad-code-org/BMAD-METHOD) | Phase-based product development flow from analysis through QA | Adopted as lifecycle phases and gates; no BMAD install by default |
| [`xmm/codex-bmad-skills`](https://github.com/xmm/codex-bmad-skills) | Codex-friendly BMAD skill packaging, intents, and YAML-backed state concepts | Adopted as routing inspiration; project does not add `bmad/` state or installer dependency by default |
| [`wshobson/agents`](https://github.com/wshobson/agents) | Multi-harness plugin marketplace with many agents, skills, commands, and orchestrators | Adopted as catalog and progressive-disclosure inspiration; no marketplace install required |
| [`NicholasSpisak/claude-code-subagents`](https://github.com/NicholasSpisak/claude-code-subagents) | Domain and keyword-based agent decision matrix | Adopted as service type plus phase routing matrix |
| [`FoundationAgents/MetaGPT`](https://github.com/FoundationAgents/MetaGPT) | Software-company style roles and collaboration model | Reference-only; no runtime dependency |
| [`OpenBMB/ChatDev`](https://github.com/OpenBMB/ChatDev) | Configurable multi-agent collaboration and virtual software company concept | Reference-only; no runtime dependency |
| [`rahulvrane/awesome-claude-agents`](https://github.com/rahulvrane/awesome-claude-agents) | Directory of subagent examples | Discovery reference only |
| [`VRSEN/agency-swarm`](https://github.com/VRSEN/agency-swarm) | Explicit role definitions and directional communication flows | Reference-only; no OpenAI API or framework dependency in default path |
| [`PabloLION/bmad-plugin`](https://github.com/PabloLION/bmad-plugin) | BMAD plugin packaging for Claude Code | Packaging reference only |

## Adopted principles

- Broad coverage is useful, but routing must remain focused.
- The Product Factory needs both technical and business agents.
- Phase-based workflow prevents jumping straight from idea to code.
- Reviewer agents should be explicit for security, QA, UX, release, compliance, and copy.
- External frameworks are useful references but too heavy for the default template path.

## Not adopted by default

- External installers
- API-backed agent runtimes
- external slash command registries
- BMAD project state folders
- agency-swarm, MetaGPT, or ChatDev execution
- copied prompt bodies or role files

## Source attribution

The local role files are original, short Codex-native configurations written for this repository. They cite the external projects in documentation only and do not reproduce full external prompts, examples, assets, or command bodies.
