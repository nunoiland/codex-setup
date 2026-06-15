# Codex External Pattern Optimization PRD

## Goal
Strengthen codex-setting by adopting safe, opt-in operating patterns from selected external agent, skill, harness, codebase-understanding, taste, and copy-quality projects without adding default dependencies, provider keys, or GitHub Actions requirements.

## Scope
- Add a documented external pattern review for the five source repositories.
- Add role plugin, codebase knowledge graph, taste/copy quality, verification loop, and external tool opt-in contracts.
- Add specialist agents for copy quality, codebase cartography, and verification loops.
- Add local skills for anti-slop copy review, frontend taste review, codebase understanding, and verification-loop review.
- Extend operator readiness with optional env flags for external tools and missing-tool warnings.
- Update README, docs index, runtime env docs, and validation guards so the new layer remains visible and safe.

## Non-goals
- Do not install external packages, CLIs, MCP servers, plugins, Figma, Chromatic, or visual SaaS.
- Do not require `OPENAI_API_KEY` or any provider key in GitHub Actions.
- Do not copy large external repository content into this repository.
- Do not run external code-generation, knowledge-graph, ECC, or plugin commands by default.
- Do not weaken approval gates, secret boundaries, protected branch safety, or validation requirements.

## Context
The current repository already contains PRD-first delivery, worktree-first workflow, API-key-free Actions, Hermes/Paperclip/Graphiti contracts, Product Factory docs, senior design layer, runtime memory, and self-improvement proposals. The external repositories add useful patterns, but a full install would increase dependency and maintenance risk. The right integration is a strong opt-in layer that codifies the useful ideas while keeping normal validation simple.

## Constraints
- GitHub Actions must remain API-key-free and must not require optional external services.
- Missing external tools must report `not_configured` or warnings in readiness, never block normal PR validation.
- External ideas must be summarized and attributed, not copied wholesale.
- Any future real install or dependency addition requires separate human approval.

## Acceptance criteria
1. New PRD, plan, docs, agents, and skills exist for the external pattern layer.
2. Operator readiness reports external tool mode, knowledge graph mode, taste/copy review levels, and verification loop mode.
3. Default readiness stays ready with local-only defaults and no open optional setup risks.
4. Optional env toggles can surface missing external tools as warnings or optional risks with no blockers.
5. README and docs index explain when to use the new layer.
6. Validation confirms workflows still do not require API keys or optional services.

## Edge cases
- `CODEX_EXTERNAL_TOOLS_MODE=opt-in` with no external CLIs installed.
- `CODEX_UNDERSTAND_ANYTHING_MODE=local` with no local path configured.
- `CODEX_UNDERSTAND_ANYTHING_MODE=committed-json` with no graph committed yet.
- Unsupported env values for taste, copy, verification, or knowledge graph modes.
- UI-heavy projects that should use taste review but have no runnable UI yet.
- Large repos where a knowledge graph would be useful but too costly to generate during CI.

## Platform target
codex-setting runtime and docs

## Delivery mode
existing repository + branch + PR

## Reporting mode
github-first local handoff

## Secret profile
No new secrets are required. External tools, provider keys, plugin credentials, API keys, SaaS tokens, and webhook URLs must stay outside tracked files. Future real installs require separate approval and a secret-boundary review.

## Human handoff
- Review the new docs and agents before using them as default operating guidance.
- Decide separately before installing any external CLIs or committing knowledge graph artifacts.
- Keep GitHub Actions API-key-free after merge.

## Validation commands
```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
CODEX_EXTERNAL_TOOLS_MODE=opt-in CODEX_UNDERSTAND_ANYTHING_MODE=local CODEX_VERIFICATION_LOOP_MODE=local python3 -m codex_runtime --operator-readiness --pretty
```

## Done when
- The external pattern layer is documented, discoverable, and represented in readiness output.
- Default validation still passes without external services or provider keys.
- Optional external tool modes produce actionable readiness output without blocking normal PR validation.
