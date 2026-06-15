# Auth Precedence

Use this precedence for Phase 2 dry-run planning and future implementation.

## GitHub

Preferred precedence:

1. `CODEX_GITHUB_AUTH_MODE=app` with all required App fields present
2. `CODEX_GITHUB_AUTH_MODE=pat` with a fine-grained PAT present
3. implicit App readiness if App fields are present and no mode is set
4. implicit PAT readiness if PAT is present and no mode is set
5. otherwise, `none`

## Provider key

- Phase-1 GitHub Actions do not require `OPENAI_API_KEY`.
- Local Codex work uses the operator's local Codex app or CLI authentication, not repository secrets.
- If a future model-backed CI workflow is enabled, `OPENAI_API_KEY` must be treated as externally injected runtime state.
- If that future key is absent, model-backed execution should be reported as blocked rather than silently assumed.

## Reporting transport

- Reporting is local handoff generation only.
- No external notification credentials are required.

## Policy

- If delivery is requested but GitHub credentials are not ready, the run is blocked.
- Even when credentials are ready, live execution stays off unless `CODEX_ENABLE_LIVE_GITHUB=1`.
- The current local executor reuses existing `gh` or `git` authentication context; it does not turn GitHub App env fields into a logged-in CLI session by itself.
- Auth precedence should be deterministic and visible in handoff output.
- GitHub App readiness requires a readable private key path, not just a non-empty variable.
