#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

umask 077

PYTHON_BIN="${CODEX_CRON_PYTHON:-python3}"
MODE="${CODEX_CRON_MODE:-queue}"
CWD="${CODEX_CRON_CWD:-$ROOT}"
LOG_FILE="${CODEX_CRON_LOG_FILE:-$ROOT/codex_runtime_state/logs/cron-runner.log}"
LOCK_DIR="${CODEX_CRON_LOCK_DIR:-$ROOT/codex_runtime_state/cron-runner.lock}"
MAX_RUNS="${CODEX_CRON_MAX_RUNS:-1}"
MAX_IDLE_CYCLES="${CODEX_CRON_MAX_IDLE_CYCLES:-1}"
POLL_SECONDS="${CODEX_CRON_POLL_SECONDS:-1}"

log() {
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" >&2
}

case "$MODE" in
  queue)
    ;;
  *)
    log "Invalid CODEX_CRON_MODE: $MODE. Expected queue."
    exit 64
    ;;
esac

mkdir -p "$ROOT/codex_runtime_state"
if [[ "$LOG_FILE" != "-" ]]; then
  mkdir -p "$(dirname "$LOG_FILE")"
  exec >>"$LOG_FILE" 2>&1
fi

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  log "Another cron runner is active; exiting without work."
  exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT

log "Starting codex cron runner in queue mode for $CWD."

"$PYTHON_BIN" -m codex_runtime \
  --cwd "$CWD" \
  --worker-loop \
  --max-runs "$MAX_RUNS" \
  --max-idle-cycles "$MAX_IDLE_CYCLES" \
  --poll-seconds "$POLL_SECONDS" \
  --pretty

log "Finished codex cron runner."
