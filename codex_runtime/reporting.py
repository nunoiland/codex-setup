from __future__ import annotations

from pathlib import Path

from .models import ReportingDispatch, RunPlan, StrategySection
from .strategy import hydrate_plan_context, slugify
from .runner import load_prd_sections


def _status_for(plan: RunPlan) -> str:
    if plan.blockers:
        return "blocked"
    if plan.warnings:
        return "partial-success"
    return "success"


def _platform_lines(plan: RunPlan) -> list[str]:
    lines = []
    for slice_ in plan.slices:
        lines.append(f"- {slice_.platform}: planned via {', '.join(slice_.builders)}")
    if not lines:
        lines.append("- unresolved: no platform slices resolved")
    return lines


def _validation_lines(plan: RunPlan) -> tuple[str, str, str]:
    commands: list[str] = []
    passed: list[str] = []
    failed: list[str] = []
    if plan.builder_execution:
        for item in plan.builder_execution:
            if item.command:
                commands.append(" ".join(item.command))
            if item.success:
                passed.append(f"{item.platform} builder execution")
            if item.errors:
                failed.extend(f"{item.platform}: {err}" for err in item.errors)
    if plan.github_delivery and plan.github_delivery.executed_commands:
        commands.extend(" ".join(cmd) for cmd in plan.github_delivery.executed_commands)
    not_run = []
    if not commands:
        not_run.append("No live execution commands were run; this remains a dry-run or prepare-only handoff.")
    return (
        "\n".join(f"- {cmd}" for cmd in commands) or "- none",
        "\n".join(f"- {item}" for item in passed) or "- none",
        "\n".join(f"- {item}" for item in failed) or "- none",
    ) if not_run == [] else (
        "\n".join(f"- {cmd}" for cmd in commands) or "- none",
        "\n".join(f"- {item}" for item in passed) or "- none",
        "\n".join(f"- {item}" for item in failed + not_run) or "- none",
    )


def _render_strategy_section(section: StrategySection) -> str:
    options = []
    for idx, option in enumerate(section.options, start=1):
        tradeoffs = "\n".join(f"    - {item}" for item in option.tradeoffs) or "    - none"
        next_actions = "\n".join(f"    - {item}" for item in option.next_actions) or "    - none"
        options.append(
            "\n".join(
                [
                    f"{idx}. {option.name} [{option.priority}]",
                    f"   - Summary: {option.summary}",
                    f"   - Rationale: {option.rationale}",
                    f"   - Expected upside: {option.expected_upside}",
                    "   - Tradeoffs:",
                    tradeoffs,
                    "   - Next actions:",
                    next_actions,
                ]
            )
        )
    notes = "\n".join(f"- {note}" for note in section.notes) or "- none"
    return "\n".join(
        [
            f"#### {section.bot}",
            f"- Focus: {section.focus}",
            f"- Recommendation: {section.recommendation}",
            f"- Notes:\n{notes}",
            f"- Options:\n" + "\n".join(options),
        ]
    )


def render_handoff(plan: RunPlan) -> str:
    title, sections = load_prd_sections(plan.prd_path)
    hydrate_plan_context(plan, sections)
    delivery = plan.github_delivery
    pr_link = delivery.pr_url if delivery and delivery.pr_url else "not created"
    repo_name = delivery.repository_name if delivery else "unknown"
    branch_name = delivery.branch_name if delivery else "unknown"
    head_sha = delivery.head_sha if delivery and delivery.head_sha else "unknown"
    status = _status_for(plan)
    warnings = "\n".join(f"- {item}" for item in plan.warnings) or "- none"
    blockers = "\n".join(f"- {item}" for item in plan.blockers) or "- none"
    validation_commands, validation_passed, validation_failed = _validation_lines(plan)
    product = plan.product_state
    product_state = "\n".join(
        [
            f"- Goal: {product.product_goal}",
            f"- Target user: {product.target_user}",
            f"- Problem: {product.problem_statement}",
            f"- Stage: {product.current_stage}",
            "- Next actions:",
            *(f"  - {item}" for item in product.next_actions),
        ]
    ) if product else "- not captured"
    qa_risks = "\n".join(f"- {item}" for item in (product.qa_risks if product else [])) or "- none"
    lessons = "\n".join(
        f"- [{note.priority}] {note.summary} — {note.recommended_follow_up}" for note in plan.lessons_learned
    ) or "- none"
    proposals = "\n".join(
        f"- {proposal.title}: {proposal.summary}" for proposal in plan.self_improvement_proposals
    ) or "- none"
    strategy_body = "\n\n".join(_render_strategy_section(section) for section in plan.strategy_sections) or "- no strategy sections prepared"
    return f"""# Morning Handoff

## 1. Run summary
- Run name: {title}
- Source PRD: {plan.prd_path}
- Platform target: {plan.platform_target}
- Delivery mode: {plan.delivery_mode}
- Reporting mode: {plan.reporting_mode}
- Overall status: {status}

## 2. GitHub artifacts
- Repository: {repo_name}
- Working branch: {branch_name}
- Head SHA: {head_sha}
- Draft PR link: {pr_link}

## 3. Platform status
{chr(10).join(_platform_lines(plan))}

## 4. Validation results
- Commands run:
{validation_commands}
- Passed:
{validation_passed}
- Failed or not run:
{validation_failed}

## 5. Product state
{product_state}

## 6. QA checklist
{qa_risks}

## 7. Risks and blockers
- Warnings:
{warnings}
- Blockers:
{blockers}

## 8. Lessons learned
{lessons}

## 9. Product and business drafts
{strategy_body}

## 10. Self-improvement proposals
{proposals}
"""


def render_summary(plan: RunPlan) -> str:
    title, sections = load_prd_sections(plan.prd_path)
    hydrate_plan_context(plan, sections)
    delivery = plan.github_delivery
    pr_link = delivery.pr_url if delivery and delivery.pr_url else "not created"
    status = _status_for(plan)
    platforms = " ".join(f"{slice_.platform}✅" for slice_ in plan.slices) or "unresolved"
    top_blocker = plan.blockers[0] if plan.blockers else "none"
    next_actions = ", ".join((plan.product_state.next_actions if plan.product_state else [])[:3]) or "review QA, choose one strategy test"
    return "\n".join(
        [
            f"Overnight run: {status}",
            f"PR: {pr_link}",
            f"Platforms: {platforms}",
            f"Top blocker: {top_blocker}",
            f"Today: {next_actions}",
        ]
    )


def prepare_reporting(plan: RunPlan, cwd: str | Path, live_mode: bool = False) -> ReportingDispatch:
    worktree = Path(cwd).resolve()
    slug = slugify(plan.title)
    handoff_path = worktree / "codex_runtime_state" / "handoff" / f"{slug}.md"
    handoff_path.parent.mkdir(parents=True, exist_ok=True)
    handoff_path.write_text(render_handoff(plan))
    dispatch = ReportingDispatch(
        requested_mode=plan.reporting_mode,
        live_mode=live_mode,
        handoff_path=str(handoff_path),
        summary_text=render_summary(plan),
    )
    if live_mode:
        dispatch.notes.append("Local handoff rendering completed; no external notification dispatch is attempted.")
    return dispatch
