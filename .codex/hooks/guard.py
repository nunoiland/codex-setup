#!/usr/bin/env python3
import json
import os
import re
import shlex
import subprocess
import sys


VALIDATION_PATTERNS = [
    r"(^|\s)(npm|pnpm|yarn|bun)\s+(run\s+)?(test|lint|typecheck|check)\b",
    r"(^|\s)pytest\b",
    r"(^|\s)ruff\b",
    r"(^|\s)mypy\b",
    r"(^|\s)cargo\s+(test|clippy|fmt)\b",
    r"(^|\s)go\s+test\b",
    r"(^|\s)make\s+(test|lint|check)\b",
    r"(^|\s)gradle(w)?\s+.*(test|lint|check)\b",
    r"(^|\s)xcodebuild\b.*\b(test|build)\b",
    r"(^|\s)swift\s+test\b",
    r"(^|\s)bundle\s+exec\s+rspec\b",
    r"(^|\s)python(3)?\s+-m\s+py_compile\b",
    r"(^|\s)(\./)?scripts/validate\.sh\b",
]

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"ASIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{36,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk_live_[A-Za-z0-9]+",
    r"sk_test_[A-Za-z0-9]+",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"xox[baprs]-[A-Za-z0-9-]{10,}",
    r"\b\d{8,10}:[A-Za-z0-9_-]{35,}\b",
    r"-----BEGIN (RSA |EC |OPENSSH |)?PRIVATE KEY-----",
]

RISKY_COMMAND_PATTERNS = [
    (r"(^|[;&|]\s*|\s)git\s+rm(\s|$)", "deleting files"),
    (r"(^|[;&|]\s*|\s)rm(\s|$)", "deleting files"),
    (r"(^|[;&|]\s*|\s)find\b.*\s-delete(\s|$)", "deleting files"),
    (r"(^|[;&|]\s*|\s)pnpm\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)yarn\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)bun\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)cargo\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)go\s+get(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)bundle\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)poetry\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)uv\s+add(\s|$)", "adding dependencies"),
    (r"(^|[;&|]\s*|\s)prisma\s+migrate\b", "running migrations"),
    (r"(^|[;&|]\s*|\s)alembic\s+(revision|upgrade)\b", "running migrations"),
    (r"(^|[;&|]\s*|\s)rails\s+(generate\s+migration|db:migrate)\b", "running migrations"),
    (r"(^|[;&|]\s*|\s)knex\s+migrate\b", "running migrations"),
    (r"(^|[;&|]\s*|\s)manage\.py\s+(makemigrations|migrate)\b", "running migrations"),
    (r"(^|[;&|]\s*|\s)git\s+reset\b", "destructive git actions"),
    (r"(^|[;&|]\s*|\s)git\s+clean\b", "destructive git actions"),
    (r"(^|[;&|]\s*|\s)git\s+checkout\s+--\b", "destructive git actions"),
    (r"(^|[;&|]\s*|\s)git\s+restore\b", "destructive git actions"),
    (r"(^|[;&|]\s*|\s)git\s+branch\s+-D\b", "destructive git actions"),
    (r"(^|[;&|]\s*|\s)git\s+worktree\s+remove\b", "destructive git actions"),
    (r"(^|[;&|]\s*|\s)git\s+push\b.*(--force|-f)\b", "force pushing"),
    (r"(^|[;&|]\s*|\s)git\s+push\b.*\s--delete\b", "risky remote mutations"),
    (r"(^|[;&|]\s*|\s)gh\s+pr\s+merge\b", "merging pull requests"),
    (r"(^|[;&|]\s*|\s)gh\s+repo\s+(create|delete|edit)\b", "risky remote mutations"),
    (r"(^|[;&|]\s*|\s)gh\s+(secret|variable)\s+set\b", "secrets or environment handling"),
    (r"(^|[;&|]\s*|\s)(vercel\s+deploy|netlify\s+deploy|fly\s+deploy|flyctl\s+deploy|wrangler\s+deploy)\b", "deployment changes"),
    (r"(^|[;&|]\s*|\s)(terraform\s+apply|kubectl\s+apply|helm\s+(install|upgrade))\b", "deployment changes"),
]

DEFAULT_PROTECTED_BRANCHES = {"main", "master"}


def read_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def exit_json(payload):
    sys.stdout.write(json.dumps(payload))
    sys.exit(0)


def command_failed(tool_response):
    if not isinstance(tool_response, dict):
        return False
    for key in ("exit_code", "exitCode", "code"):
        value = tool_response.get(key)
        if isinstance(value, int):
            return value != 0
    output = tool_response.get("output")
    if isinstance(output, dict):
        for key in ("exit_code", "exitCode", "code"):
            value = output.get(key)
            if isinstance(value, int):
                return value != 0
    return False


def is_validation_command(command):
    if not command:
        return False
    return any(re.search(pattern, command) for pattern in VALIDATION_PATTERNS)


def get_current_branch(cwd):
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        return (result.stdout or "").strip()
    except Exception:
        return ""


def classify_risky_command(command, cwd="."):
    if not command:
        return None

    normalized = " ".join(command.strip().split())
    try:
        tokens = shlex.split(normalized)
    except ValueError:
        tokens = []

    if tokens[:2] == ["npm", "install"] and len(tokens) > 2:
        return "adding dependencies"
    if tokens[:2] == ["npm", "i"] and len(tokens) > 2:
        return "adding dependencies"
    if tokens[:2] == ["pip", "install"]:
        return "adding dependencies"
    if tokens[:2] == ["git", "push"] and any(token in {"--force", "-f"} for token in tokens[2:]):
        return "force pushing"
    if tokens[:2] == ["git", "push"]:
        protected_branches = get_protected_branches()
        current_branch = get_current_branch(cwd)
        for token in tokens[2:]:
            if token_targets_protected_branch(token, protected_branches):
                return "pushing directly to protected branches"
        if "HEAD" in tokens[2:] and current_branch in protected_branches:
            return "pushing directly to protected branches"

    for pattern, reason in RISKY_COMMAND_PATTERNS:
        if re.search(pattern, normalized):
            return reason

    return None


def scan_git_diff_for_secrets(cwd):
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--", "."],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        diff_text = result.stdout or ""
        if not diff_text:
            result = subprocess.run(
                ["git", "diff", "--", "."],
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
            )
            diff_text = result.stdout or ""
    except Exception:
        return []

    findings = []
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, diff_text):
            findings.append(pattern)
    return findings


def get_protected_branches():
    configured = os.getenv("CODEX_PROTECTED_BRANCHES", "").strip()
    if not configured:
        return DEFAULT_PROTECTED_BRANCHES
    branches = {item.strip() for item in configured.split(",") if item.strip()}
    return branches or DEFAULT_PROTECTED_BRANCHES


def token_targets_protected_branch(token, protected_branches):
    if token in protected_branches:
        return True
    if token.startswith("refs/heads/") and token.removeprefix("refs/heads/") in protected_branches:
        return True
    for branch in protected_branches:
        if token.endswith(f":{branch}") or token.endswith(f":refs/heads/{branch}"):
            return True
    return False


def handle_session_start(payload):
    return {
        "systemMessage": (
            "PRD-driven, worktree-first repository: read the active PRD first, write or update a plan before medium or large work, "
            "keep changes inside the current worktree, keep the local repo and GitHub as the source of truth, keep external operator channels off the default path, "
            "and report validation honestly."
        )
    }


def handle_pre_tool_use(payload):
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command", "")
    risk = classify_risky_command(command, payload.get("cwd") or ".")

    if risk:
        return {
            "decision": "block",
            "reason": (
                f"This repository requires explicit user approval before {risk}. "
                "Ask the user first, then continue only after confirmation."
            ),
            "stopReason": f"user approval required for {risk}",
        }

    return {}


def handle_post_tool_use(payload):
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command", "")
    tool_response = payload.get("tool_response") or {}

    if is_validation_command(command) and command_failed(tool_response):
        return {
            "decision": "block",
            "reason": (
                "A mandatory validation command failed. Fix the failure or explain why "
                "the validation is intentionally not passing before continuing."
            ),
            "stopReason": "mandatory validation failed",
        }

    secret_hits = scan_git_diff_for_secrets(payload.get("cwd") or ".")
    if secret_hits:
        return {
            "systemMessage": (
                "Potential secret leakage patterns were detected in the current diff. "
                "Review the diff carefully before continuing."
            )
        }

    return {}


def handle_stop(payload):
    cwd = payload.get("cwd") or "."
    secret_hits = scan_git_diff_for_secrets(cwd)
    message = (
        "Before final output, summarize PRD alignment, files changed, exact validation commands run, unsupported or removed config keys, approvals still needed, and remaining risk. "
        "Confirm the local repo and GitHub remained canonical and that any optional external operator path stayed outside the default workflow."
    )
    if secret_hits:
        message += (
            " Also review the diff for possible secret leakage before shipping; the hook detected text matching common secret formats."
        )
    return {"systemMessage": message}


def main():
    payload = read_input()
    event_name = payload.get("hook_event_name")

    if event_name == "SessionStart":
        exit_json(handle_session_start(payload))
    if event_name == "PreToolUse":
        exit_json(handle_pre_tool_use(payload))
    if event_name == "PostToolUse":
        exit_json(handle_post_tool_use(payload))
    if event_name == "Stop":
        exit_json(handle_stop(payload))

    exit_json({})


if __name__ == "__main__":
    main()
