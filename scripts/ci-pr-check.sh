#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RUN_ID="${GITHUB_RUN_ID:-local-$(date -u '+%Y%m%dT%H%M%SZ')}"
EVIDENCE_DIR="${CODEX_CI_EVIDENCE_DIR:-$ROOT/codex_runtime_state/actions/$RUN_ID}"
LOG_DIR="$EVIDENCE_DIR/logs"
CHECKS_FILE="$EVIDENCE_DIR/checks.jsonl"

mkdir -p "$LOG_DIR"
: >"$CHECKS_FILE"

record_check() {
  local name="$1"
  local status="$2"
  local command_text="$3"
  local log_path="$4"

  python3 - "$CHECKS_FILE" "$name" "$status" "$command_text" "$log_path" <<'PY'
from pathlib import Path
import json
import sys

checks_file = Path(sys.argv[1])
record = {
    "name": sys.argv[2],
    "status": int(sys.argv[3]),
    "command": sys.argv[4],
    "log": sys.argv[5],
}
with checks_file.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, sort_keys=True) + "\n")
PY
}

redact_log() {
  local log_path="$1"
  python3 - "$log_path" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="replace")
patterns = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{16,}"), "sk-REDACTED"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{16,}"), "gh_REDACTED"),
    (
        re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*['\"]?[^'\"\s]+"),
        lambda match: f"{match.group(1)}=REDACTED",
    ),
]
for pattern, replacement in patterns:
    text = pattern.sub(replacement, text)
path.write_text(text, encoding="utf-8")
PY
}

run_check() {
  local name="$1"
  shift
  local log_path="$LOG_DIR/$name.log"
  local command_text="$*"

  {
    printf 'command: %s\n' "$command_text"
    printf 'started_at: %s\n\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  } >"$log_path"

  set +e
  "$@" >>"$log_path" 2>&1
  local status=$?
  set -e

  {
    printf '\nfinished_at: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    printf 'exit_code: %s\n' "$status"
  } >>"$log_path"

  redact_log "$log_path"

  record_check "$name" "$status" "$command_text" "$log_path"

  if [[ "$status" -eq 0 ]]; then
    echo "$name-ok"
  else
    echo "$name-failed"
  fi

  return "$status"
}

FAILED=0

if ! CODEX_VALIDATE_REQUIRE_CODEX="${CODEX_VALIDATE_REQUIRE_CODEX:-0}" run_check validate ./scripts/validate.sh; then
  FAILED=1
fi

if ! run_check whitespace git diff --check; then
  FAILED=1
fi

if ! run_check web-health-smoke ./scripts/web-health-smoke.sh; then
  FAILED=1
fi

if ! CODEX_BROWSER_QA_ARTIFACT_DIR="$EVIDENCE_DIR/browser-qa" run_check browser-qa ./scripts/browser-qa.sh; then
  FAILED=1
fi

./scripts/harness-dry-run.sh --evidence-dir "$EVIDENCE_DIR"

if [[ "$FAILED" -ne 0 ]]; then
  echo "ci-pr-check-failed: evidence at $EVIDENCE_DIR" >&2
  exit 1
fi

echo "ci-pr-check-ok: evidence at $EVIDENCE_DIR"
