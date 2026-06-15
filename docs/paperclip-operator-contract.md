# Paperclip Operator Contract

Paperclip is the preferred future operator layer for running `codex-setting` across many products.

## Role

Paperclip should manage:

- goals and product initiatives
- task tickets
- assigned workers
- recurring routines
- budget and approval policy
- audit history

GitHub remains the source of truth for code, PRs, checks, and reviewable delivery artifacts.

## Mapping

| Product Factory concept | Paperclip concept |
| --- | --- |
| Product PRD | Goal or task context |
| Implementation request | Issue assigned to a worker |
| Local Codex/Hermes worker | Agent employee |
| Harness evidence | Work product or artifact |
| Human approval | Board or approval gate |
| Merge decision | GitHub PR review and label |
| Runtime memory update | Task notes plus external memory backend |

## Required behavior

- Paperclip must not bypass GitHub branch protection.
- Paperclip must not inject secrets into tracked files.
- Paperclip should create or reference work tickets, not silently mutate protected branches.
- Paperclip is optional until explicitly configured with `CODEX_PAPERCLIP_BASE_URL` and, for local API checks, `CODEX_PAPERCLIP_API_URL`.

## Environment

```bash
CODEX_OPERATOR_PLATFORM=paperclip
CODEX_PAPERCLIP_BASE_URL=
CODEX_PAPERCLIP_API_URL=
CODEX_PAPERCLIP_HERMES_AGENT_NAME=Hermes Engineer
```

Suggested local API value when Paperclip is actually running:

```bash
CODEX_PAPERCLIP_API_URL=http://127.0.0.1:3100/api
```

If Paperclip is missing or unreachable, readiness should warn but normal validation should pass.

## Local connection readiness

The readiness command should check:

- Node.js availability
- `npx` or `pnpm` availability
- Paperclip API reachability
- configured Hermes agent name

Paperclip should be run from its own checkout or package setup, not vendored into this repository.
