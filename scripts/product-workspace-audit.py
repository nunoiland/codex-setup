#!/usr/bin/env python3
"""Fail if product-specific workspaces are accidentally placed in codex_set.

The repository is a settings/template OS. Real products should live in sibling
repositories or worktrees, not as top-level product folders inside this repo.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_TOP_LEVEL_DIRS = {
    ".agents",
    ".codex",
    ".git",
    ".github",
    ".next",
    "PLANS",
    "PRD",
    "codex_runtime",
    "codex_runtime_state",
    "coverage",
    "docs",
    "node_modules",
    "out",
    "scripts",
    "src",
    "__pycache__",
}

PRODUCT_PLATFORM_DIRS = {
    "android",
    "app",
    "ios",
    "server",
    "backend",
    "mobile",
}

PRODUCT_MARKER_FILES = {
    "AGENTS.md",
    "README.md",
    "package.json",
    "build.gradle.kts",
    "settings.gradle.kts",
    "pyproject.toml",
    "go.mod",
    "Cargo.toml",
}


def git_ls_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def has_any(path: Path, names: set[str]) -> bool:
    return any((path / name).exists() for name in names)


def is_product_like(path: Path) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    if (path / ".git").exists():
        reasons.append("contains its own .git directory")

    if (path / "PRD").is_dir() and (path / "PLANS").is_dir():
        reasons.append("contains PRD/ and PLANS/ directories")

    platform_dirs = sorted(name for name in PRODUCT_PLATFORM_DIRS if (path / name).is_dir())
    if platform_dirs and has_any(path, PRODUCT_MARKER_FILES | {"PRD", "PLANS"}):
        reasons.append(f"contains product platform directories: {', '.join(platform_dirs)}")

    nested_product_markers = []
    children = path.iterdir() if path.exists() else []
    for child in children:
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (child / "PRD").is_dir() and (child / "PLANS").is_dir():
            nested_product_markers.append(str(child.relative_to(ROOT)))
    if nested_product_markers:
        reasons.append("contains nested product markers: " + ", ".join(nested_product_markers))

    return bool(reasons), reasons


def main() -> int:
    tracked_files = git_ls_files()
    failures: list[str] = []

    for child in sorted(ROOT.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if child.name in ALLOWED_TOP_LEVEL_DIRS:
            continue
        if child.name.startswith("."):
            continue

        product_like, reasons = is_product_like(child)
        if not product_like:
            continue

        tracked_under_dir = any(
            item == child.name or item.startswith(f"{child.name}/")
            for item in tracked_files
        )
        tracked_label = "tracked" if tracked_under_dir else "untracked"
        failures.append(
            f"- {child.relative_to(ROOT)} ({tracked_label}): " + "; ".join(reasons)
        )

    if failures:
        message = "\n".join(
            [
                "Product workspace boundary violation detected.",
                "Move product-specific repositories outside codex_set or intentionally convert them into sibling repos/worktrees.",
                "Detected:",
                *failures,
                "See docs/product-workspace-boundary.md for the supported flow.",
            ]
        )
        print(message, file=sys.stderr)
        return 1

    print("product-workspace-boundary-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
