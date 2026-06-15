#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

LABEL = "automerge-approved"
SUCCESS_CONCLUSIONS = {"success", "neutral", "skipped"}


def fail(message: str) -> None:
    print(f"automerge-blocked: {message}", file=sys.stderr)
    raise SystemExit(1)


def github_request(method: str, path: str, payload: dict | None = None) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token:
        fail("GITHUB_TOKEN is required.")
    if not repo:
        fail("GITHUB_REPOSITORY is required.")

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = Request(
        f"https://api.github.com{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            details = json.loads(body).get("message") or body
        except json.JSONDecodeError:
            details = body
        fail(f"GitHub API {method} {path} failed with HTTP {error.code}: {details}")


def load_event() -> dict:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        fail("GITHUB_EVENT_PATH is required.")
    with open(event_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def latest_check_by_name(check_runs: list[dict]) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for run in check_runs:
        name = run.get("name")
        if not name:
            continue
        previous = latest.get(name)
        current_time = run.get("completed_at") or run.get("started_at") or ""
        previous_time = ""
        if previous:
            previous_time = previous.get("completed_at") or previous.get("started_at") or ""
        if previous is None or current_time >= previous_time:
            latest[name] = run
    return latest


def assert_required_checks(repo: str, sha: str) -> None:
    required = [
        name.strip()
        for name in os.environ.get("CODEX_AUTOMERGE_REQUIRED_CHECKS", "pr-validate").split(",")
        if name.strip()
    ]
    if not required:
        fail("At least one required check name must be configured.")

    payload = github_request("GET", f"/repos/{repo}/commits/{sha}/check-runs?per_page=100")
    latest = latest_check_by_name(payload.get("check_runs", []))
    missing: list[str] = []
    incomplete: list[str] = []
    failed: list[str] = []

    for name in required:
        run = latest.get(name)
        if run is None:
            missing.append(name)
            continue
        if run.get("status") != "completed":
            incomplete.append(f"{name} ({run.get('status')})")
            continue
        if run.get("conclusion") not in SUCCESS_CONCLUSIONS:
            failed.append(f"{name} ({run.get('conclusion')})")

    if missing:
        fail(f"required checks are missing for head SHA {sha}: {', '.join(missing)}")
    if incomplete:
        fail(f"required checks are not complete: {', '.join(incomplete)}")
    if failed:
        fail(f"required checks did not pass: {', '.join(failed)}")


def main() -> None:
    event = load_event()
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        fail("GITHUB_REPOSITORY is required.")

    pr = event.get("pull_request")
    if not pr and event.get("workflow_run"):
        workflow_run = event["workflow_run"]
        if workflow_run.get("conclusion") != "success":
            fail(f"PR Validate did not succeed: {workflow_run.get('conclusion')}")
        pull_requests = workflow_run.get("pull_requests") or []
        if not pull_requests:
            fail("workflow_run payload does not reference a pull request.")
        pr_number = pull_requests[0].get("number")
        if not pr_number:
            fail("workflow_run pull request payload is missing a number.")
        pr = github_request("GET", f"/repos/{repo}/pulls/{pr_number}")

    if not pr:
        fail("This workflow must run from pull_request_target or workflow_run.")

    labels = {label.get("name") for label in pr.get("labels", [])}
    if LABEL not in labels:
        fail(f"label `{LABEL}` is required.")
    if pr.get("draft"):
        fail("draft PRs are not eligible for automerge.")

    head_repo = pr.get("head", {}).get("repo", {}).get("full_name")
    base_repo = pr.get("base", {}).get("repo", {}).get("full_name")
    if head_repo != base_repo:
        fail("automerge only supports branches from the same repository.")

    head_sha = pr.get("head", {}).get("sha")
    number = pr.get("number")
    if not head_sha or not number:
        fail("pull request payload is missing number or head SHA.")

    assert_required_checks(repo, head_sha)

    merge_payload = {
        "commit_title": f"Merge PR #{number}: {pr.get('title') or 'Codex-setting update'}",
        "merge_method": "squash",
    }
    result = github_request("PUT", f"/repos/{repo}/pulls/{number}/merge", merge_payload)
    if not result.get("merged"):
        fail(f"GitHub did not merge the PR: {result}")

    print(f"automerge-merged: PR #{number}")


if __name__ == "__main__":
    main()
