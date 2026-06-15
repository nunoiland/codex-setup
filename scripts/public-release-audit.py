#!/usr/bin/env python3
"""Check the current tree for obvious public-release blockers.

This audit checks the current repository contents only. It does not prove that
Git history is clean; use a clean public branch or separate public repo before
making a repository public.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

IGNORED_PARTS = {
    ".git",
    ".next",
    "coverage",
    "node_modules",
    "out",
    "codex_runtime_state",
}

SELF = Path("scripts/public-release-audit.py")

BLOCKED_TERMS = {
    "duedoc": "extracted product reference",
    "fitness league": "extracted product reference",
    "hidnap.com": "personal domain reference",
    "codex_" + "tele" + "gram": "retired messenger env reference",
    "codex_" + "chat" + "ops": "retired messenger env reference",
}

SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "OpenAI-style API key"),
    (re.compile(r"ghp_[A-Za-z0-9_]{20,}"), "GitHub token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"), "Slack token"),
    (re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*=\s*['\"]?(?!$|<|placeholder|changeme|redacted|example)[^'\"\s#]{8,}"), "non-placeholder secret assignment"),
]

LOCAL_PATH_PATTERNS = [
    (re.compile(r"/Users/(?!<)[A-Za-z0-9._-]+/"), "macOS user home path"),
    (re.compile(r"/home/(?!<)[A-Za-z0-9._-]+/"), "Linux user home path"),
]


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    files: list[Path] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = Path(line.strip())
        if path == SELF:
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        full_path = ROOT / path
        if full_path.is_file():
            files.append(path)
    return sorted(files, key=str)


def read_text(path: Path) -> str | None:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def main() -> int:
    findings: list[str] = []

    for path in candidate_files():
        text = read_text(path)
        if text is None:
            continue
        lowered = text.lower()

        for term, reason in BLOCKED_TERMS.items():
            if term in lowered:
                findings.append(f"{path}: {reason}: {term}")

        for pattern, reason in LOCAL_PATH_PATTERNS:
            for match in pattern.finditer(text):
                findings.append(f"{path}: {reason}: {match.group(0)}")

        for pattern, reason in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                snippet = match.group(0)
                line_start = text.rfind("\n", 0, match.start()) + 1
                line_end = text.find("\n", match.end())
                if line_end == -1:
                    line_end = len(text)
                line = text[line_start:line_end]
                if any(env_source in line for env_source in ("os.environ", "process.env", "env.get(")):
                    continue
                if len(snippet) > 80:
                    snippet = snippet[:77] + "..."
                findings.append(f"{path}: {reason}: {snippet}")

    if findings:
        print("Public release audit failed.", file=sys.stderr)
        print("Fix current-tree blockers before creating a public branch:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        print("Note: this audit does not clean Git history.", file=sys.stderr)
        return 1

    print("public-release-current-tree-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
