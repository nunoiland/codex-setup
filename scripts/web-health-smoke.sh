#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PORT="${CODEX_HEALTH_SMOKE_PORT:-3100}"
HOST="${CODEX_HEALTH_SMOKE_HOST:-127.0.0.1}"
LOG_FILE="${CODEX_HEALTH_SMOKE_LOG:-/tmp/codex-template-health-smoke.log}"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
    wait "$SERVER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

pnpm exec next start --hostname "$HOST" --port "$PORT" >"$LOG_FILE" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 30); do
  if curl --silent --fail "http://$HOST:$PORT/health" >/tmp/codex-template-health-response.json 2>/dev/null; then
    python3 - <<'PY'
from pathlib import Path
import json

payload = json.loads(Path("/tmp/codex-template-health-response.json").read_text(encoding="utf-8"))
if payload.get("status") != "ok":
    raise SystemExit(f"unexpected health payload: {payload}")
print("health-smoke-ok")
PY
    exit 0
  fi
  sleep 1
done

if grep -qE 'listen EPERM|Operation not permitted' "$LOG_FILE" 2>/dev/null; then
  python3 - <<'PY'
from pathlib import Path

route_file = Path("src/app/health/route.ts")
text = route_file.read_text(encoding="utf-8")
required = ['status: "ok"', "NextResponse.json", "template: true"]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"health route fallback verification failed: {missing}")
print("health-smoke-skipped-sandbox")
PY
  exit 0
fi

echo "health-smoke-failed" >&2
cat "$LOG_FILE" >&2 || true
exit 1
