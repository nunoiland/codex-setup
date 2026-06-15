# Paperclip + Hermes Local Runbook

Use this runbook when you are ready to try Paperclip as the local Product Factory operator and Hermes as a managed worker.

This is optional. Normal PR validation must pass without Paperclip, Hermes, provider keys, Docker, or Node services.

## Local target

Paperclip local default:

```bash
http://localhost:3100
http://127.0.0.1:3100/api
```

Readiness command:

```bash
CODEX_HERMES_ADAPTER_MODE=paperclip python3 -m codex_runtime --operator-readiness --pretty
```

## Expected local tools

- Node.js
- `npx` or `pnpm`
- `hermes` command when using Hermes locally
- provider API key injected outside this repository when actually running Hermes

Do not commit provider keys, Paperclip secrets, local tokens, Hermes config, or `.env` files.

## Suggested Paperclip setup

Paperclip can be started locally through its own project setup. Keep that checkout outside this repository.

Recommended local agent:

```json
{
  "name": "Hermes Engineer",
  "adapterType": "hermes_local",
  "adapterConfig": {
    "timeoutSec": 300,
    "persistSession": true,
    "worktreeMode": true,
    "checkpoints": true,
    "enabledToolsets": ["terminal", "file", "web"]
  }
}
```

## Product Factory worker prompt shape

Assign tasks that include:

- PRD path or task goal
- repository path
- target branch or worktree rule
- validation commands
- approval boundaries
- expected PR handoff
- instruction to keep GitHub Actions API-key-free

## Safe failure behavior

If readiness reports Paperclip or Hermes as missing:

- keep using the local Codex app
- keep local JSON memory
- keep GitHub PR validation as the merge gate
- treat Paperclip/Hermes as optional until the local service is configured
