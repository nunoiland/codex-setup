# Cron Runner

Use `scripts/cron-runner.sh` when this repository needs a local scheduler entry that safely wakes the runtime and checks queued work.

## What it does

- Runs the local queue worker with bounded runs and idle cycles.
- Uses a lock directory to avoid overlapping runs.
- Writes logs to `codex_runtime_state/logs/cron-runner.log` by default.
- Keeps live builder and GitHub execution behind the existing explicit enable flags.

## Examples

```bash
# Drain at most one eligible queued run.
CODEX_CRON_MODE=queue ./scripts/cron-runner.sh

# Print the worker output to stdout for validation.
CODEX_CRON_LOG_FILE=- CODEX_CRON_MODE=queue ./scripts/cron-runner.sh
```

Crontab example:

```cron
* * * * * cd /path/to/codex-setting && CODEX_CRON_MODE=queue /path/to/codex-setting/scripts/cron-runner.sh
```

## Environment

| Variable | Default | Notes |
| --- | --- | --- |
| `CODEX_CRON_MODE` | `queue` | Only `queue` is supported. |
| `CODEX_CRON_CWD` | repository root | Runtime cwd for queue processing. |
| `CODEX_CRON_PYTHON` | `python3` | Python executable. |
| `CODEX_CRON_LOG_FILE` | `codex_runtime_state/logs/cron-runner.log` | Use `-` for stdout/stderr. |
| `CODEX_CRON_LOCK_DIR` | `codex_runtime_state/cron-runner.lock` | Lock directory path. |
| `CODEX_CRON_MAX_RUNS` | `1` | Maximum queued runs per invocation. |
| `CODEX_CRON_MAX_IDLE_CYCLES` | `1` | Empty queue polls before exit. |
| `CODEX_CRON_POLL_SECONDS` | `1` | Delay between idle polls. |

## Safety

- Keep live builder and live GitHub execution disabled until the live validation playbook passes.
- Treat cron as a wake-up mechanism, not an approval bypass.
- Use GitHub and local handoff artifacts as the review record.
