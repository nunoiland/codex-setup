# Product Factory Evolution Layer Plan

## Summary

Add a conservative Product Factory operating layer for `codex-setting` without changing the current API-key-free GitHub Actions path. Paperclip is the preferred future operator dashboard, Hermes is introduced as an adapter contract only, and Graphiti with Neo4j is prepared as an opt-in long-term memory backend while local JSON remains the default.

## Key tasks

1. Add runtime readiness output for operator platform, Hermes adapter mode, memory backend, Graphiti readiness, Paperclip readiness, and GitHub Actions API-key-free assumptions.
2. Add documentation contracts for Product Factory operations, Paperclip mapping, Hermes worker boundaries, and Graphiti memory episodes.
3. Add environment placeholders and runtime-env documentation for the new opt-in surfaces.
4. Tighten validation so normal PR checks do not require Paperclip, Hermes, Graphiti, Docker, Neo4j, or API keys.
5. Add local Paperclip + Hermes readiness for the `paperclip` adapter mode without installing or running external services.
6. Add `/goal` intake contract and risk register so default setup has no open optional-service risks.

## Validation

Run:

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
CODEX_MEMORY_BACKEND=graphiti python3 -m codex_runtime --operator-readiness --pretty
CODEX_HERMES_ADAPTER_MODE=paperclip python3 -m codex_runtime --operator-readiness --pretty
git diff --check
```

## Non-goals

- Do not install Paperclip, Hermes, Graphiti, Neo4j, or Docker.
- Do not add new package dependencies.
- Do not require any API key in GitHub Actions.
- Include existing local virtual idol docs/PRD/plan in the eventual PR unchanged unless a separate validation issue requires a targeted docs-index adjustment.
