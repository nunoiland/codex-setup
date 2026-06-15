# Product Factory Risk Register

This register keeps optional Product Factory risks explicit without making normal PR validation depend on external services.

## Resolved by default

- GitHub Actions remain API-key-free.
- Local JSON memory remains the default backend.
- Paperclip, Hermes, Graphiti, Neo4j, Docker, Caddy, PostgreSQL, Stripe, and Toss Payments are not required for PR validation.
- `/goal` has a stable intake contract.
- Service basecamp contracts are docs/readiness only until a template scaffold is explicitly approved.
- Missing optional services are readiness warnings, not blockers.

## Open only when optional modes are enabled

| Risk | When it appears | Safe response |
| --- | --- | --- |
| Paperclip API is unreachable | `CODEX_HERMES_ADAPTER_MODE=paperclip` and Paperclip is not running | Start Paperclip outside this repo or continue with local Codex app |
| Hermes command is missing | `CODEX_HERMES_ADAPTER_MODE=local` or `paperclip` | Install Hermes locally or set `CODEX_HERMES_COMMAND` |
| Provider key is missing | Hermes execution mode is enabled | Inject key locally or via self-hosted secret store only |
| Graphiti is not configured | `CODEX_MEMORY_BACKEND=graphiti` | Start Graphiti/Neo4j or return to `CODEX_MEMORY_BACKEND=json` |
| Service template is not scaffolded | A future product needs a runnable starter app | Create a separate approved template PR |
| Unsupported mode is configured | Any Product Factory env var uses an unsupported value | Return to the documented safe defaults in `.env.example` |

## Non-negotiable controls

- No provider keys in tracked files.
- No Paperclip or Hermes dependency in GitHub-hosted Actions.
- No auto-merge of self-improvement proposals.
- No production, auth, payment, deployment, or destructive changes without explicit approval.

## Readiness commands

```bash
python3 -m codex_runtime --operator-readiness --pretty
CODEX_HERMES_ADAPTER_MODE=paperclip python3 -m codex_runtime --operator-readiness --pretty
CODEX_MEMORY_BACKEND=graphiti python3 -m codex_runtime --operator-readiness --pretty
```
