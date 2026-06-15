# Hermes Worker Contract

Hermes Agent is the preferred future managed worker target, but this repository does not require Hermes for normal operation.

## Current phase

- Mode: `contract`
- Execution: disabled by default
- Secrets: local or self-hosted only
- GitHub Actions: no Hermes dependency

## Worker input

A Hermes-compatible worker should receive:

- PRD path or task ticket
- repository path
- target branch
- validation commands
- approval boundaries
- expected handoff format
- optional memory context

## Worker output

A worker should produce:

- focused code/doc changes
- validation results
- failure evidence when blocked
- PR-ready handoff notes
- proposed memory updates
- self-improvement proposals as drafts only

## Allowed boundaries

Hermes may operate inside an approved local workspace or worktree. It must not:

- commit secrets
- bypass GitHub PR review
- force-push
- merge protected branches
- weaken validation or approval gates
- make production, auth, payment, or deployment changes without explicit approval

## Environment

```bash
CODEX_HERMES_ADAPTER_MODE=contract
CODEX_HERMES_COMMAND=hermes
```

Supported modes:

- `contract`: document and validate the worker contract only
- `disabled`: no Hermes worker path
- `local`: local Hermes command may be used by an operator, outside GitHub Actions
- `paperclip`: Hermes is expected to run through the Paperclip local adapter path

## Paperclip adapter target

When `CODEX_HERMES_ADAPTER_MODE=paperclip`, the preferred adapter shape is:

- package: `hermes-paperclip-adapter`
- adapter type: `hermes_local`
- agent name: `Hermes Engineer`
- session persistence: enabled
- worktree isolation: enabled
- checkpoints: recommended

Missing Hermes command, provider keys, or Paperclip API reachability should produce readiness warnings only.
