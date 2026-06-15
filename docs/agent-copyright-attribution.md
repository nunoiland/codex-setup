# Agent Copyright and Attribution Boundary

The Agent Army layer is source-attributed but locally rewritten.

## Policy

- Do not copy external agent prompt bodies, examples, assets, or long role files into this repository.
- Use external repos for taxonomy, routing, workflow, and packaging inspiration only.
- Keep local agents short, Codex-native, and aligned to this repo's PRD-first and validation-first rules.
- Preserve trademark boundaries for named methods such as BMAD.
- If future work imports external files, it needs a separate PRD, license review, and explicit approval.

## License notes

- `msitarzewski/agency-agents`: MIT-licensed repository according to its GitHub page.
- `bmad-code-org/BMAD-METHOD`: MIT License with BMAD trademark notice.
- `xmm/codex-bmad-skills`: MIT License and BMAD attribution.
- `wshobson/agents`: MIT-licensed marketplace with Codex-compatible plugin patterns.
- `NicholasSpisak/claude-code-subagents`: used as an agent decision matrix reference; check individual files before importing anything.
- `FoundationAgents/MetaGPT`: MIT-licensed framework, reference-only here.
- `OpenBMB/ChatDev`: Apache-2.0-licensed framework, reference-only here.
- `rahulvrane/awesome-claude-agents`: MIT for the directory, with possible per-file attribution differences.
- `VRSEN/agency-swarm`: MIT-licensed framework, reference-only here.
- `PabloLION/bmad-plugin`: MIT License with BMAD trademark notice.

## Practical rule

When adding a new local agent, write it from this repo's needs:

1. define the job in one sentence
2. list boundaries and approval rules
3. state expected output
4. avoid external prose reuse
5. cite source inspiration in docs, not in every prompt
