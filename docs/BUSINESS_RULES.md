# Business Rules

These rules are durable and should not change silently.

- GitHub is the system of record for code, review state, validation history, and handoff artifacts.
- local handoff is an operator console, not the authoritative record.
- Secrets must come from external environment or secret management, never tracked files.
- Strategy, pricing, launch, and revenue output are drafts for human review.
- Protected branches require explicit human intent.
- Auth, payment, schema, env, deploy, deletion, and irreversible actions always require explicit approval.
- When in doubt, prefer safe dry-run behavior over live execution.
