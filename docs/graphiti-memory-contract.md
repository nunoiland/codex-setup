# Graphiti Memory Contract

Graphiti with Neo4j is the preferred long-term memory direction for product decisions and evolving product facts. Local JSON remains the default backend.

## Current phase

- Default backend: `json`
- Optional backend: `graphiti`
- Preferred Graphiti database: Neo4j via Docker
- GitHub Actions requirement: none

## Memory episodes

When Graphiti is enabled, record episodes for:

- product decisions
- PRD changes
- validation failures
- QA risks
- release notes
- growth experiments
- pricing hypotheses
- launch hypotheses
- repeated lessons
- approved self-improvement proposals

## Source-of-truth rule

Graphiti memory helps future runs retrieve context, but it does not replace:

- GitHub PRs
- validation logs
- harness artifacts
- human approvals
- tracked docs

## Environment

```bash
CODEX_MEMORY_BACKEND=json
CODEX_GRAPHITI_BASE_URL=
CODEX_GRAPHITI_GROUP_ID=
```

Use `CODEX_MEMORY_BACKEND=graphiti` only when a local or self-hosted Graphiti service is ready.

## Optional Neo4j setup direction

Graphiti commonly runs with Neo4j. Keep any real credentials outside the repository. A product or operator machine may use Docker Compose or another local service manager, but normal `codex-setting` validation must not require Docker.

## Fallback

If Graphiti is missing or unreachable, the runtime should report readiness warnings and keep local JSON as the safe fallback.
