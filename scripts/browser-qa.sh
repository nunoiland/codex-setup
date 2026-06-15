#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ARTIFACT_DIR="${CODEX_BROWSER_QA_ARTIFACT_DIR:-$ROOT/codex_runtime_state/browser-qa}"
URL="${CODEX_WEB_QA_URL:-}"
COMMAND="${CODEX_WEB_QA_COMMAND:-}"

mkdir -p "$ARTIFACT_DIR"

write_result() {
  local status="$1"
  local reason="$2"
  local log_path="${3:-}"

  python3 - "$ARTIFACT_DIR" "$status" "$reason" "$log_path" "$URL" "$COMMAND" <<'PY'
from pathlib import Path
import json
import os
import sys

artifact_dir = Path(sys.argv[1])
status = sys.argv[2]
reason = sys.argv[3]
log_path = sys.argv[4]
url = sys.argv[5]
command = sys.argv[6]

payload = {
    "status": status,
    "reason": reason,
    "url": url or None,
    "command_configured": bool(command),
    "log_path": log_path or None,
}

(artifact_dir / "browser-qa.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

summary_lines = [
    "# Browser QA",
    "",
    f"- Status: `{status}`",
    f"- Reason: {reason}",
]
if url:
    summary_lines.append(f"- URL: `{url}`")
if log_path:
    summary_lines.append(f"- Log: `{os.path.relpath(log_path, artifact_dir)}`")

(artifact_dir / "browser-qa-summary.md").write_text(
    "\n".join(summary_lines) + "\n",
    encoding="utf-8",
)
PY
}

if [[ -z "$URL" && -z "$COMMAND" ]]; then
  write_result "skipped" "No CODEX_WEB_QA_URL or CODEX_WEB_QA_COMMAND was configured."
  echo "browser-qa-skipped"
  exit 0
fi

if [[ -n "$COMMAND" ]]; then
  LOG_PATH="$ARTIFACT_DIR/browser-qa-command.log"
  set +e
  bash -lc "$COMMAND" >"$LOG_PATH" 2>&1
  STATUS=$?
  set -e

  if [[ "$STATUS" -eq 0 ]]; then
    write_result "passed" "Configured browser QA command completed successfully." "$LOG_PATH"
  else
    write_result "failed" "Configured browser QA command failed with exit code $STATUS." "$LOG_PATH"
  fi
  exit "$STATUS"
fi

LOG_PATH="$ARTIFACT_DIR/browser-qa-url.log"
if command -v curl >/dev/null 2>&1; then
  set +e
  curl -I --fail --silent --show-error --max-time "${CODEX_WEB_QA_TIMEOUT_SECONDS:-15}" "$URL" >"$LOG_PATH" 2>&1
  STATUS=$?
  set -e
else
  set +e
  python3 - "$URL" >"$LOG_PATH" 2>&1 <<'PY'
from urllib.request import Request, urlopen
import sys

url = sys.argv[1]
request = Request(url, method="HEAD")
with urlopen(request, timeout=15) as response:
    print(f"status={response.status}")
PY
  STATUS=$?
  set -e
fi

if [[ "$STATUS" -eq 0 ]]; then
  write_result "passed" "Configured web QA target responded successfully." "$LOG_PATH"
else
  write_result "failed" "Configured web QA target failed with exit code $STATUS." "$LOG_PATH"
fi

exit "$STATUS"
