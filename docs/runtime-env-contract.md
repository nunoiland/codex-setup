# Runtime Environment Contract

Use this file together with [`../.env.example`](../.env.example). The tracked file contains placeholders only.

## Principles

- real values never belong in the repository
- each variable should have one clear owner
- delivery credentials and provider credentials should stay separated
- prefer GitHub App flows over broad personal tokens
- strategy and self-improvement output should remain drafts for human review

## Variables

| Variable | Purpose | Notes |
| --- | --- | --- |
| `CODEX_GITHUB_AUTH_MODE` | Selects GitHub auth style | Prefer `app`; use `pat` only when needed |
| `CODEX_GITHUB_APP_ID` | GitHub App identifier | Placeholder only |
| `CODEX_GITHUB_INSTALLATION_ID` | GitHub App installation target | Placeholder only |
| `CODEX_GITHUB_PRIVATE_KEY_PATH` | Local path to injected private key | Never commit the key file |
| `CODEX_GITHUB_PAT` | Fine-grained PAT fallback | Use only when GitHub App is not practical |
| `CODEX_ENABLE_LIVE_GITHUB` | Opt-in switch for live GitHub execution | Keep `0` by default |
| `CODEX_GITHUB_REPOSITORY` | Optional `owner/name` override for delivery | Falls back to cwd name if omitted |
| `CODEX_GITHUB_REMOTE` | Remote name used for live push operations | Defaults to `origin` |
| `CODEX_GITHUB_REPO_VISIBILITY` | Visibility used for repo creation | Example: `private`, `public` |
| `OPENAI_API_KEY` | Future provider key for model-backed CI runs | Not required in phase 1; inject externally only when explicitly enabling API-backed automation |
| `CODEX_VALIDATE_REQUIRE_CODEX` | Whether validation must fail if local `codex` CLI is missing | Use `0` in GitHub Actions; use `1` only for local Codex setup checks |
| `CODEX_CI_EVIDENCE_DIR` | Override for CI evidence output | Defaults under `codex_runtime_state/actions` |
| `CODEX_WEB_QA_URL` | Optional web URL for browser QA smoke check | Empty means browser QA is skipped with evidence |
| `CODEX_WEB_QA_COMMAND` | Optional browser or Playwright QA command | Use for product repositories with real web QA |
| `CODEX_WEB_QA_TIMEOUT_SECONDS` | Timeout for URL smoke check | Defaults to `15` |
| `CODEX_BROWSER_QA_ARTIFACT_DIR` | Override for browser QA artifacts | Defaults under `codex_runtime_state/browser-qa` or CI evidence |
| `CODEX_AUTOMERGE_REQUIRED_CHECKS` | Comma-separated check names required before automerge | Defaults to `pr-validate` |
| `CODEX_OPERATOR_PLATFORM` | Optional Product Factory operator platform | Defaults to `paperclip`; normal PR validation does not require it |
| `CODEX_PAPERCLIP_BASE_URL` | Optional Paperclip UI/base URL for readiness output | Empty means Paperclip UI is not configured |
| `CODEX_PAPERCLIP_API_URL` | Optional Paperclip API URL for local readiness checks | Empty by default; suggested local value is `http://127.0.0.1:3100/api` |
| `CODEX_PAPERCLIP_HERMES_AGENT_NAME` | Suggested Paperclip agent name for Hermes worker setup | Defaults to `Hermes Engineer` |
| `CODEX_HERMES_ADAPTER_MODE` | Hermes worker integration mode | Defaults to `contract`; supported: `contract`, `disabled`, `local`, `paperclip` |
| `CODEX_HERMES_COMMAND` | Hermes CLI command used for local readiness checks | Defaults to `hermes` |
| `CODEX_MEMORY_BACKEND` | Runtime memory backend | Defaults to `json`; supported: `json`, `graphiti` |
| `CODEX_GRAPHITI_BASE_URL` | Optional Graphiti service base URL | Required only when actually using Graphiti |
| `CODEX_GRAPHITI_GROUP_ID` | Optional Graphiti group or namespace id | Required only when actually using Graphiti |
| `CODEX_EXTERNAL_TOOLS_MODE` | Optional external pattern tool mode | Defaults to `off`; supported: `off`, `opt-in` |
| `CODEX_UNDERSTAND_ANYTHING_MODE` | Optional codebase knowledge graph mode | Defaults to `off`; supported: `off`, `local`, `committed-json` |
| `CODEX_UNDERSTAND_ANYTHING_PATH` | Optional local checkout or binary path for knowledge graph tooling | Empty means not configured |
| `CODEX_TASTE_REVIEW_LEVEL` | Design taste review strictness | Defaults to `standard`; supported: `standard`, `strict` |
| `CODEX_COPY_REVIEW_LEVEL` | Copy quality review strictness | Defaults to `standard`; supported: `standard`, `strict` |
| `CODEX_VERIFICATION_LOOP_MODE` | Verification-loop mode | Defaults to `contract`; supported: `contract`, `local` |
| `CODEX_ENABLE_BUILDER_EXECUTION` | Opt-in switch for live builder command execution | Keep `0` by default |
| `CODEX_WEB_BUILDER_COMMAND` | Local command used for the web slice | Example wrapper script or CLI |
| `CODEX_IOS_BUILDER_COMMAND` | Local command used for the iOS slice | Example wrapper script or CLI |
| `CODEX_ANDROID_BUILDER_COMMAND` | Local command used for the Android slice | Example wrapper script or CLI |
| `CODEX_API_BUILDER_COMMAND` | Local command used for the API slice | Example wrapper script or CLI |
| `CODEX_REPORTING_MODE` | Local handoff contract | Use `github_only` |
| `CODEX_DEFAULT_GITHUB_OWNER` | Default owner or org | Optional convenience value |
| `CODEX_DEFAULT_BASE_BRANCH` | Default base branch for delivery | Usually `main` |
| `CODEX_PROTECTED_BRANCHES` | Comma-separated branches treated as protected by local guardrails | Defaults to `main,master` |

## Operational guidance

### GitHub

- Prefer GitHub App credentials for repository creation, branch creation, push, and PR creation.
- If `CODEX_GITHUB_PAT` is used, keep it fine-grained and narrow in scope.
- Do not set both GitHub App and PAT paths unless the operator clearly understands precedence.
- For the current local executor, App fields do not automatically authenticate `gh`; use an already authenticated CLI context or an approved PAT fallback.
- Phase-1 PR validation, harness, and automerge use `GITHUB_TOKEN` only. They do not require `OPENAI_API_KEY`.

### Product Factory operator layer

- Paperclip, Hermes, and Graphiti are optional in this phase.
- `python3 -m codex_runtime --operator-readiness --pretty` reports missing services as readiness warnings.
- `CODEX_HERMES_ADAPTER_MODE=paperclip python3 -m codex_runtime --operator-readiness --pretty` checks local Paperclip and Hermes readiness without running an agent.
- Do not put Paperclip, Hermes, Graphiti, Neo4j, provider API keys, or worker credentials in tracked files.
- GitHub-hosted Actions should remain API-key-free; local or self-hosted workers may inject secrets outside the repository.

### External pattern layer

- `CODEX_EXTERNAL_TOOLS_MODE=off` is the default.
- `CODEX_EXTERNAL_TOOLS_MODE=opt-in` only changes readiness reporting; it does not install or run external tools.
- `CODEX_UNDERSTAND_ANYTHING_MODE=local` may point to an approved local checkout through `CODEX_UNDERSTAND_ANYTHING_PATH`.
- `CODEX_UNDERSTAND_ANYTHING_MODE=committed-json` expects reviewed and sanitized `.understand-anything` artifacts.
- `CODEX_TASTE_REVIEW_LEVEL=strict` and `CODEX_COPY_REVIEW_LEVEL=strict` should be used for public, pricing, investor, regulated, or trust-sensitive surfaces.
- `CODEX_VERIFICATION_LOOP_MODE=local` means a local harness may assist after approval; normal validation must still work without it.
- Missing optional external tools must produce readiness warnings or optional risks, not GitHub Actions blockers.

### Builders

- Builder commands are local operator-supplied commands, not tracked code.
- Keep `CODEX_ENABLE_BUILDER_EXECUTION=0` unless you intend to run them live.
- Prefer wrapper scripts outside tracked secrets and keep per-platform commands minimal and reviewable.

### Scheduling and retries

- Keep delayed scheduling bounded and local-first in this phase.
- Prefer small retry limits so repeated failures become explicit review items.
- Use lessons-learned output to decide whether to retry, not just a timer.

## Ownership checklist

For each real deployment of this template, define:

- who owns each variable
- where the real value is stored
- who can rotate it
- what breaks if it expires
