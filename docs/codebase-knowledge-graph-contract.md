# Codebase Knowledge Graph Contract

This contract defines how optional codebase knowledge graphs may be used for large product repositories.

## Goal

Help Codex and humans understand unfamiliar or large codebases before implementation. The graph should teach architecture, ownership, and flow. It should not become required CI infrastructure.

## Modes

| Mode | Meaning |
| --- | --- |
| `off` | Default. No graph expected. |
| `local` | A human-approved local tool may generate or read graph artifacts outside normal validation. |
| `committed-json` | A repo may commit sanitized graph JSON for onboarding and PR review. |

## Env surface

- `CODEX_UNDERSTAND_ANYTHING_MODE=off|local|committed-json`
- `CODEX_UNDERSTAND_ANYTHING_PATH=` optional local checkout or binary path

## Safe usage

Use a graph when:

- the repo is too large to inspect quickly
- architecture boundaries are unclear
- onboarding a new service into Product Factory
- planning a cross-platform or cross-layer refactor
- reviewing high-risk flows such as auth, billing, admin, or data pipelines

Avoid a graph when:

- the task is small and local
- a normal search gives enough context
- graph generation would require secrets, network access, or long CI runtime

## Artifact policy

- Do not commit raw intermediate scratch files.
- Do not commit secrets, private URLs, customer data, or generated content that includes proprietary samples.
- Large committed graphs should use Git LFS only after approval.
- Keep graph output advisory; the codebase remains the source of truth.

## Readiness behavior

Missing local tools or graph artifacts must report `not_configured` or warnings only. Normal PR validation must not fail because the graph is absent.
