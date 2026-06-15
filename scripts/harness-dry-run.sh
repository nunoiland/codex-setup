#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

EVIDENCE_DIR=""

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --evidence-dir)
      if [[ "$#" -lt 2 ]]; then
        echo "missing value for --evidence-dir" >&2
        exit 64
      fi
      EVIDENCE_DIR="$2"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 64
      ;;
  esac
done

if [[ -z "$EVIDENCE_DIR" ]]; then
  EVIDENCE_DIR="$ROOT/codex_runtime_state/harness/$(date -u '+%Y%m%dT%H%M%SZ')"
fi

mkdir -p "$EVIDENCE_DIR"

python3 - "$ROOT" "$EVIDENCE_DIR" <<'PY'
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re
import subprocess
import sys

root = Path(sys.argv[1])
evidence_dir = Path(sys.argv[2])
logs_dir = evidence_dir / "logs"
checks_path = evidence_dir / "checks.jsonl"

SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{16,}"), "sk-REDACTED"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{16,}"), "gh_REDACTED"),
    (
        re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*['\"]?[^'\"\s]+"),
        lambda match: f"{match.group(1)}=REDACTED",
    ),
]


def redact(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def git_value(*args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip() or None
    except Exception:
        return None


def load_checks() -> list[dict]:
    checks: list[dict] = []
    if not checks_path.is_file():
        return checks
    for line in checks_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            checks.append(json.loads(line))
        except json.JSONDecodeError:
            checks.append(
                {
                    "name": "malformed-check-record",
                    "status": 1,
                    "command": "read checks.jsonl",
                    "log": str(checks_path),
                }
            )
    return checks


def read_log(path_text: str | None) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        return ""
    return redact(path.read_text(encoding="utf-8", errors="replace")[-12000:])


def likely_cause(log_text: str) -> str:
    lower = log_text.lower()
    if "command not found" in lower or "no such file or directory" in lower:
        return "Missing local command, file, or dependency."
    if "syntaxerror" in lower or "parse error" in lower or "bash -n" in lower:
        return "Syntax or configuration parsing failure."
    if "assertionerror" in lower or "assert " in lower:
        return "Validation assertion failed."
    if "traceback" in lower:
        return "Python runtime error during validation."
    if "timed out" in lower or "timeout" in lower:
        return "Timeout or unavailable external target."
    if "secret" in lower or "token" in lower or "api_key" in lower or "api key" in lower:
        return "Secret-boundary or credential-related failure. Inspect carefully before sharing logs."
    return "Unknown from dry-run evidence; inspect the captured log."


checks = load_checks()
failures = []
for check in checks:
    status = int(check.get("status") or 0)
    log_text = read_log(check.get("log"))
    check["log_excerpt"] = log_text[-4000:] if log_text else ""
    if status != 0:
        failures.append(
            {
                "name": check.get("name"),
                "status": status,
                "command": check.get("command"),
                "log": check.get("log"),
                "likely_cause": likely_cause(log_text),
            }
        )

overall_status = "failed" if failures else "passed"
if not checks:
    overall_status = "dry-run"

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "repository": os.environ.get("GITHUB_REPOSITORY") or git_value("config", "--get", "remote.origin.url"),
    "branch": os.environ.get("GITHUB_HEAD_REF") or git_value("branch", "--show-current"),
    "sha": os.environ.get("GITHUB_SHA") or git_value("rev-parse", "HEAD"),
    "status": overall_status,
    "checks": checks,
    "failures": failures,
    "reproduction_commands": [
        "./scripts/validate.sh",
        "git diff --check",
        "./scripts/browser-qa.sh",
    ],
    "regression_test_candidates": [
        "Keep the failing command in the PR checklist until it passes.",
        "Add a focused test for the exact failing validation path if this is product-code related.",
    ],
    "setting_improvement_candidates": [
        "If the same command fails repeatedly, move it into scripts/validate.sh or the project harness.",
        "If browser QA is skipped unintentionally, set CODEX_WEB_QA_URL or CODEX_WEB_QA_COMMAND in the product repository.",
    ],
}

(evidence_dir / "harness-evidence.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

lines = [
    "# Harness Dry-run Report",
    "",
    f"- Status: `{overall_status}`",
    f"- Generated: `{payload['generated_at']}`",
    f"- Branch: `{payload['branch'] or 'unknown'}`",
    f"- SHA: `{payload['sha'] or 'unknown'}`",
    "",
    "## Checks",
]
if checks:
    for check in checks:
        marker = "PASS" if int(check.get("status") or 0) == 0 else "FAIL"
        lines.append(f"- `{marker}` `{check.get('name')}`: `{check.get('command')}`")
else:
    lines.append("- No upstream checks were provided. This confirms report generation only.")

lines.extend(["", "## Failures"])
if failures:
    for failure in failures:
        lines.append(f"- `{failure['name']}` exited `{failure['status']}`: {failure['likely_cause']}")
        if failure.get("log"):
            lines.append(f"  Log: `{failure['log']}`")
else:
    lines.append("- No failures detected in supplied check records.")

lines.extend(
    [
        "",
        "## Reproduce Locally",
        "- `./scripts/validate.sh`",
        "- `git diff --check`",
        "- `./scripts/browser-qa.sh`",
        "",
        "## Local Codex Prompt",
        "Give local Codex the failing log and ask: `이 PR의 GitHub Actions 실패를 고쳐줘. API 키 없이 동작해야 하고, 실패 재현 명령도 같이 실행해줘.`",
        "",
        "## Improvement Candidates",
        "- Promote repeated failures into `scripts/validate.sh`.",
        "- Add a focused regression test when the failure is product behavior, not environment setup.",
        "- Configure `CODEX_WEB_QA_URL` or `CODEX_WEB_QA_COMMAND` only in product repositories that have a web target.",
    ]
)

(evidence_dir / "harness-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"harness-dry-run-ok: {evidence_dir / 'harness-summary.md'}")
PY
