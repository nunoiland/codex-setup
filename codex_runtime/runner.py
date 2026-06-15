from __future__ import annotations

import os
import re
from pathlib import Path

from .models import AuthStatus, DeliveryStatus, PlatformSlice, ReportingStatus, RunPlan
from .strategy import hydrate_plan_context

SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)

PLATFORM_BUILDERS: dict[str, list[str]] = {
    "web": ["web_builder"],
    "ios": ["ios_builder"],
    "android": ["android_builder"],
    "api": ["api_builder"],
}

VALIDATION_HINTS: dict[str, str] = {
    "web": "frontend lint/test/typecheck/build",
    "ios": "xcodebuild or swift build/test",
    "android": "gradle lint/test/build",
    "api": "backend lint/test/type or service checks",
}


def load_prd_sections(prd_path: str | Path) -> tuple[str, dict[str, str]]:
    path = Path(prd_path)
    text = path.read_text()
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, str] = {}
    for i, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    title = text.splitlines()[0].lstrip("#").strip()
    return title, sections


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        value = line.strip()
        if value:
            return value.removeprefix("-").strip()
    return ""


def _normalize_platform_target(raw: str) -> tuple[str, list[str], list[str]]:
    value = raw.strip().lower()
    if not value:
        return "", [], ["Missing platform target."]

    if value == "multi-platform":
        return value, [], [
            "Platform target is 'multi-platform'; a human or higher-level orchestrator must resolve exact slices from PRD scope."
        ]

    parts = [part.strip() for part in value.split("+") if part.strip()]
    unique_parts: list[str] = []
    blockers: list[str] = []
    for part in parts:
        if part not in PLATFORM_BUILDERS:
            blockers.append(f"Unsupported platform target slice: {part}")
            continue
        if part not in unique_parts:
            unique_parts.append(part)
    return value, unique_parts, blockers


def _resolve_github_mode() -> tuple[str, bool]:
    env_mode = os.getenv("CODEX_GITHUB_AUTH_MODE", "").strip().lower()
    private_key_path = os.getenv("CODEX_GITHUB_PRIVATE_KEY_PATH", "").strip()
    private_key_ready = bool(private_key_path) and Path(private_key_path).expanduser().is_file() and os.access(
        Path(private_key_path).expanduser(), os.R_OK
    )
    has_app = all(
        os.getenv(name)
        for name in (
            "CODEX_GITHUB_APP_ID",
            "CODEX_GITHUB_INSTALLATION_ID",
        )
    ) and private_key_ready
    has_pat = bool(os.getenv("CODEX_GITHUB_PAT"))

    if env_mode == "app":
        return "app", has_app
    if env_mode == "pat":
        return "pat", has_pat
    if has_app:
        return "app", True
    if has_pat:
        return "pat", True
    return "none", False


def _build_auth_status() -> AuthStatus:
    github_mode, github_ready = _resolve_github_mode()
    provider_ready = bool(os.getenv("OPENAI_API_KEY"))
    return AuthStatus(
        github_mode=github_mode,
        github_ready=github_ready,
        provider_ready=provider_ready,
    )


def _build_delivery_status(delivery_mode: str, auth: AuthStatus) -> DeliveryStatus:
    lowered = delivery_mode.lower()
    repo_create = "new repository" in lowered
    branch_delivery = "branch" in lowered or "draft pr" in lowered
    return DeliveryStatus(
        requested_mode=delivery_mode,
        can_attempt_repo_create=repo_create and auth.github_ready,
        can_attempt_branch_delivery=branch_delivery and auth.github_ready,
    )


def _build_reporting_status(reporting_mode: str) -> ReportingStatus:
    return ReportingStatus(
        requested_mode=reporting_mode,
    )


def build_run_plan(prd_path: str | Path) -> RunPlan:
    title, sections = load_prd_sections(prd_path)
    raw_platform_target = _first_nonempty_line(sections.get("Platform target", ""))
    raw_delivery_mode = sections.get("Delivery mode", "").strip() or "github_only_unknown_delivery"
    raw_reporting_mode = sections.get("Reporting mode", "").strip() or "github_only"

    normalized_target, slices_requested, blockers = _normalize_platform_target(raw_platform_target)
    auth = _build_auth_status()
    delivery = _build_delivery_status(raw_delivery_mode, auth)
    reporting = _build_reporting_status(raw_reporting_mode)

    slices: list[PlatformSlice] = []
    if normalized_target and normalized_target != "multi-platform":
        for platform in slices_requested:
            slices.append(
                PlatformSlice(
                    platform=platform,
                    builders=PLATFORM_BUILDERS[platform],
                    validation_hint=VALIDATION_HINTS[platform],
                )
            )

    notes: list[str] = []
    warnings: list[str] = []
    if ("new repository" in raw_delivery_mode.lower() or "branch" in raw_delivery_mode.lower()) and not auth.github_ready:
        blockers.append("GitHub delivery is requested, but GitHub runtime credentials are not ready.")
    if normalized_target != "multi-platform" and len(slices) > 1:
        notes.append("This is a multi-slice run; preserve partial-success reporting per platform.")
    if normalized_target == "multi-platform":
        notes.append(
            "Exact slice resolution is deferred because platform target is 'multi-platform'; use PRD scope to decide slices."
        )
    notes.append(
        "This runtime defaults to dry-run planning; live GitHub delivery requires explicit opt-in, and reporting renders local handoff artifacts."
    )
    notes.append("Strategy outputs are drafts for human review and should never be treated as automatic business decisions.")

    plan = RunPlan(
        prd_path=str(prd_path),
        title=title,
        platform_target=normalized_target or raw_platform_target,
        delivery_mode=raw_delivery_mode,
        reporting_mode=raw_reporting_mode,
        supported=not blockers,
        slices=slices,
        blockers=blockers,
        warnings=warnings,
        notes=notes,
        auth=auth,
        delivery=delivery,
        reporting=reporting,
    )
    return hydrate_plan_context(plan, sections)
