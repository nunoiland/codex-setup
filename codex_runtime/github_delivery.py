from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from .models import GitHubDeliveryPlan, RunPlan


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "prd-run"


def _repository_name(cwd: Path) -> str:
    explicit = os.getenv("CODEX_GITHUB_REPOSITORY", "").strip()
    if explicit:
        return explicit.split("/")[-1]
    return cwd.name


def _repository_owner() -> str:
    explicit = os.getenv("CODEX_GITHUB_REPOSITORY", "").strip()
    if "/" in explicit:
        return explicit.split("/")[0]
    return os.getenv("CODEX_DEFAULT_GITHUB_OWNER", "").strip()


def _base_branch() -> str:
    return os.getenv("CODEX_DEFAULT_BASE_BRANCH", "main").strip() or "main"


def _remote_name() -> str:
    return os.getenv("CODEX_GITHUB_REMOTE", "origin").strip() or "origin"


def _commit_message(slug: str) -> str:
    return f"codex: {slug}"


def _pr_title(title: str) -> str:
    return f"[Codex] {title.strip() or 'PRD run'}"


def _branch_command(worktree: Path, branch_name: str) -> list[str]:
    exists = subprocess.run(
        ["git", "-C", str(worktree), "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        text=True,
        capture_output=True,
        check=False,
    )
    if exists.returncode == 0:
        return ["git", "-C", str(worktree), "checkout", branch_name]
    return ["git", "-C", str(worktree), "checkout", "-b", branch_name]


def render_pr_body(plan: RunPlan, live_mode: bool = False) -> str:
    slice_list = ", ".join(slice_.platform for slice_ in plan.slices) or "unresolved"
    blockers = "\n".join(f"- {item}" for item in plan.blockers) or "- none"
    warnings = "\n".join(f"- {item}" for item in plan.warnings) or "- none"
    notes = "\n".join(f"- {item}" for item in plan.notes) or "- none"
    executor_state = "enabled" if live_mode else "prepared only"
    return f"""## Source PRD
- {plan.prd_path}

## Platform target
- {plan.platform_target}

## Planned slices
- {slice_list}

## Validation status
- Runtime planning completed
- Live GitHub delivery executor {executor_state}

## Blockers
{blockers}

## Warnings
{warnings}

## Operator notes
{notes}
"""


def prepare_github_delivery(plan: RunPlan, cwd: str | Path, live_mode: bool = False) -> GitHubDeliveryPlan:
    worktree = Path(cwd).resolve()
    title_slug = _slugify(plan.title)
    branch_name = f"codex/{title_slug}"
    pr_body_path = worktree / "codex_runtime_state" / "pr" / f"{title_slug}.md"
    pr_body_path.parent.mkdir(parents=True, exist_ok=True)

    delivery = GitHubDeliveryPlan(
        cwd=str(worktree),
        repository_owner=_repository_owner(),
        repository_name=_repository_name(worktree),
        remote_name=_remote_name(),
        base_branch=_base_branch(),
        branch_name=branch_name,
        commit_message=_commit_message(title_slug),
        pr_title=_pr_title(plan.title),
        pr_body_path=str(pr_body_path),
        requested_mode=plan.delivery_mode,
        live_mode=live_mode,
        repo_create_requested="new repository" in plan.delivery_mode.lower(),
        branch_delivery_requested=("branch" in plan.delivery_mode.lower() or "draft pr" in plan.delivery_mode.lower()),
        draft_pr_requested="draft pr" in plan.delivery_mode.lower(),
    )

    pr_body_path.write_text(render_pr_body(plan, live_mode=live_mode))

    if not plan.auth or not plan.auth.github_ready:
        delivery.errors.append("GitHub credentials are not ready for live delivery.")
        delivery.notes.append("Prepared GitHub delivery metadata only.")
        return delivery

    if live_mode and os.getenv("CODEX_ENABLE_LIVE_GITHUB") != "1":
        delivery.errors.append("Live GitHub delivery is disabled. Set CODEX_ENABLE_LIVE_GITHUB=1 to execute.")
        return delivery

    if live_mode and plan.auth and plan.auth.github_mode == "app" and not os.getenv("CODEX_GITHUB_PAT"):
        delivery.warnings.append(
            "Local live execution does not bootstrap GitHub App auth into gh/git automatically. Use an existing authenticated gh/git context or provide an approved PAT fallback."
        )

    if delivery.repo_create_requested:
        visibility = os.getenv("CODEX_GITHUB_REPO_VISIBILITY", "private").strip() or "private"
        target = f"{delivery.repository_owner}/{delivery.repository_name}" if delivery.repository_owner else delivery.repository_name
        delivery.commands.append(["gh", "repo", "create", target, f"--{visibility}", "--source", str(worktree), "--remote", delivery.remote_name])
        delivery.notes.append("Repository creation is planned before branch delivery.")

    if delivery.branch_delivery_requested:
        delivery.commands.extend(
            [
                _branch_command(worktree, delivery.branch_name),
                ["git", "-C", str(worktree), "add", "-A"],
                ["git", "-C", str(worktree), "diff", "--cached", "--quiet"],
                ["git", "-C", str(worktree), "commit", "-m", delivery.commit_message],
                ["git", "-C", str(worktree), "push", "-u", delivery.remote_name, delivery.branch_name],
            ]
        )
    if delivery.draft_pr_requested:
        repo_target = f"{delivery.repository_owner}/{delivery.repository_name}" if delivery.repository_owner else delivery.repository_name
        delivery.commands.append(
            [
                "gh",
                "pr",
                "create",
                "--repo",
                repo_target,
                "--draft",
                "--base",
                delivery.base_branch,
                "--head",
                delivery.branch_name,
                "--title",
                delivery.pr_title,
                "--body-file",
                delivery.pr_body_path,
            ]
        )
    return delivery


def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    pat = os.getenv("CODEX_GITHUB_PAT", "").strip()
    if pat:
        env.setdefault("GH_TOKEN", pat)
        env.setdefault("GITHUB_TOKEN", pat)
    return subprocess.run(command, text=True, capture_output=True, check=False, env=env)


def _first_url(text: str) -> str:
    for token in text.split():
        if token.startswith("http://") or token.startswith("https://"):
            return token.strip()
    return ""


def execute_github_delivery(delivery: GitHubDeliveryPlan) -> GitHubDeliveryPlan:
    if delivery.errors:
        return delivery

    if shutil.which("git") is None:
        delivery.errors.append("git is required for live GitHub delivery execution.")
        return delivery

    needs_gh = any(command and command[0] == "gh" for command in delivery.commands)
    if needs_gh and shutil.which("gh") is None:
        delivery.errors.append("gh CLI is required for repo creation or draft PR execution.")
        return delivery

    skip_commit = False
    for command in delivery.commands:
        if command[-2:] == ["--cached", "--quiet"]:
            result = _run_command(command)
            delivery.executed_commands.append(command)
            if result.returncode == 0:
                skip_commit = True
                delivery.notes.append("No staged changes detected; skipping commit.")
            elif result.returncode == 1:
                delivery.notes.append("Staged changes detected; continuing with commit.")
            else:
                delivery.errors.append((result.stderr or result.stdout).strip() or "git diff --cached --quiet failed")
                break
            continue

        if skip_commit and command[:4] == ["git", "-C", delivery.cwd, "commit"]:
            delivery.skipped_commands.append(command)
            continue

        result = _run_command(command)
        delivery.executed_commands.append(command)
        if result.returncode != 0:
            delivery.errors.append((result.stderr or result.stdout).strip() or f"Command failed: {command}")
            break
        stdout = result.stdout.strip()
        if command[:3] == ["gh", "repo", "create"]:
            delivery.repository_url = _first_url(stdout)
        elif command[:3] == ["gh", "pr", "create"]:
            delivery.pr_url = _first_url(stdout)

    if not delivery.errors:
        head_result = _run_command(["git", "-C", delivery.cwd, "rev-parse", "HEAD"])
        if head_result.returncode == 0:
            delivery.head_sha = head_result.stdout.strip()

    return delivery
