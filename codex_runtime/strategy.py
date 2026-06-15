from __future__ import annotations

import re
from typing import Iterable

from .models import MemoryNote, ProductState, RunPlan, SelfImprovementProposal, StrategyOption, StrategySection


def slugify(value: str) -> str:
    parts = re.split(r"[^a-z0-9]+", value.lower())
    return "-".join(part for part in parts if part) or "prd-run"


def _bullet_lines(text: str) -> list[str]:
    items: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("- ", "* ")):
            items.append(line[2:].strip())
            continue
        match = re.match(r"^\d+\.\s+(.*)$", line)
        if match:
            items.append(match.group(1).strip())
    return items


def _first_nonempty_line(text: str) -> str:
    for raw in text.splitlines():
        value = raw.strip()
        if value:
            return value.lstrip("-*").strip()
    return ""


def _pick(items: Iterable[str], fallback: str, *, limit: int = 3) -> list[str]:
    values = [item.strip() for item in items if item.strip()]
    if not values:
        return [fallback]
    return values[:limit]


def _infer_target_user(goal: str, context: list[str], title: str) -> str:
    lowered = f"{goal} {' '.join(context)} {title}".lower()
    if any(word in lowered for word in ("founder", "operator", "builder", "team", "developer")):
        return "founders or operators running the product workflow"
    if any(word in lowered for word in ("shop", "seller", "merchant", "store")):
        return "operators who need a dependable service workflow"
    return "the narrowest operator group that urgently feels the product pain"


def _infer_problem(goal: str, context: list[str], title: str) -> str:
    base = goal or (context[0] if context else title)
    return base.rstrip(".")


def _stage_for(plan: RunPlan) -> str:
    if plan.blockers:
        return "blocked"
    if plan.builder_execution:
        if any(item.executed for item in plan.builder_execution):
            return "partial-success" if plan.warnings else "ready-for-review"
        return "prepared"
    if plan.reporting_dispatch or plan.github_delivery:
        return "partial-success" if plan.warnings else "prepared"
    return "planned"


def _execution_context(plan: RunPlan) -> dict[str, object]:
    successful_slices = [item.platform for item in plan.builder_execution if item.success]
    failed_slices = [item.platform for item in plan.builder_execution if item.errors]
    prepared_slices = [item.platform for item in plan.builder_execution if item.command and not item.executed]
    pr_ready = bool(plan.github_delivery and (plan.github_delivery.pr_url or plan.github_delivery.branch_name))
    handoff_ready = bool(plan.reporting_dispatch and plan.reporting_dispatch.handoff_path)
    return {
        "successful_slices": successful_slices,
        "failed_slices": failed_slices,
        "prepared_slices": prepared_slices,
        "pr_ready": pr_ready,
        "handoff_ready": handoff_ready,
    }


def _top_actions(plan: RunPlan, acceptance: list[str], handoff: list[str]) -> list[str]:
    actions = []
    if plan.blockers:
        actions.append(f"Resolve blocker: {plan.blockers[0]}")
    if plan.warnings:
        actions.append(f"Review warning: {plan.warnings[0]}")
    actions.extend(handoff)
    actions.extend(acceptance)
    deduped: list[str] = []
    for action in actions:
        if action and action not in deduped:
            deduped.append(action)
    return deduped[:5] or ["Run QA on the primary flow and confirm the release decision."]


def _strategy_sections(service_name: str, goal: str, target_user: str, problem: str, plan: RunPlan) -> list[StrategySection]:
    top_blocker = plan.blockers[0] if plan.blockers else "no blocker recorded"
    platforms = ", ".join(slice_.platform for slice_ in plan.slices) or plan.platform_target or "unresolved scope"
    context = _execution_context(plan)
    successful_slices = context["successful_slices"]
    failed_slices = context["failed_slices"]
    prepared_slices = context["prepared_slices"]
    proof_asset = "the latest GitHub handoff" if context["handoff_ready"] else "a builder log or prepared handoff draft"
    launch_state = (
        "Resolve the current blocker before pushing growth or launch activity."
        if plan.blockers
        else "Use the implementation artifact and GitHub handoff as the proof asset for the first launch test."
    )
    slice_summary = ", ".join(successful_slices or prepared_slices or ["no completed platform slices yet"])
    failure_summary = ", ".join(failed_slices) if failed_slices else "no failed slices recorded"

    positioning = StrategySection(
        bot="positioning-bot",
        focus="value proposition and narrative",
        recommendation=f"Lead with the narrow pain-first angle and support it with execution proof from {slice_summary}.",
        options=[
            StrategyOption(
                name="Narrow pain-first angle",
                summary=f"Position {service_name} as the fastest way for {target_user} to solve: {problem}.",
                rationale="A narrow promise is easier to communicate and validate in the first release window.",
                expected_upside=f"Higher message clarity and stronger conversion when backed by proof from {proof_asset}.",
                priority="high",
                tradeoffs=["May feel too narrow if the product serves multiple use cases.", "Needs disciplined scope in onboarding copy."],
                next_actions=["Write a one-line value proposition focused on the core pain.", "Test the message in the first landing page hero and local handoff summary."],
            ),
            StrategyOption(
                name="Speed and automation angle",
                summary=f"Emphasize overnight execution, reduced manual work, and faster operator throughput proven by {slice_summary}.",
                rationale="Speed is often the easiest proof point when the product automates repetitive product work.",
                expected_upside="Good fit for demos, launch posts, and product-led acquisition.",
                priority="medium",
                tradeoffs=["Can sound generic without concrete before/after examples.", "Needs proof points from actual usage logs or case studies."],
                next_actions=["Capture one before/after workflow example.", "Turn the example into launch copy and onboarding proof."],
            ),
            StrategyOption(
                name="Operator-control and trust angle",
                summary="Lead with GitHub-first records, safe approvals, and human-in-the-loop control.",
                rationale="Trust matters when the workflow touches code, release decisions, and business strategy drafts.",
                expected_upside="Better fit for technical buyers who worry about unsafe automation.",
                priority="medium",
                tradeoffs=["Less exciting than a speed-first launch story.", "Requires clear explanation of what remains manual."],
                next_actions=["Document the approval boundaries in product copy.", "Show how GitHub remains the system of record."],
            ),
        ],
        notes=[
            f"Current platform scope: {platforms}.",
            f"Execution proof currently available from: {slice_summary}.",
            f"Top blocker for messaging alignment: {top_blocker}.",
        ],
    )

    growth = StrategySection(
        bot="growth-bot",
        focus="acquisition and activation experiments",
        recommendation="Start with proof-driven acquisition that references the latest implementation result, then layer outreach and community tests.",
        options=[
            StrategyOption(
                name="Founder-led direct outreach",
                summary=f"Reach out to small groups of {target_user} with a short demo or screenshot based on {proof_asset}.",
                rationale="Direct conversations reveal positioning gaps and real objections faster than broad campaigns.",
                expected_upside="Fastest route to early user feedback and first paying conversations.",
                priority="high",
                tradeoffs=["Manual and hard to scale.", "Requires the founder or operator to stay close to user feedback."],
                next_actions=["Build a 10-person target list.", "Send a concise pain-first message with one proof artifact."],
            ),
            StrategyOption(
                name="Proof-driven content loop",
                summary=f"Publish implementation proof, handoff screenshots, and learnings from {slice_summary} as repeatable content.",
                rationale="The product is strongest when it can show work completed, not just describe intent.",
                expected_upside="Creates reusable content for SEO, Threads and launch assets.",
                priority="high",
                tradeoffs=["Needs consistent content packaging.", "Proof content can expose product rough edges if QA is weak."],
                next_actions=["Turn the latest run result into one short case study.", "Repurpose the case study into three channel-specific posts."],
            ),
            StrategyOption(
                name="Community or partner distribution",
                summary="Offer a limited beta through founder communities, operator groups, or workflow-heavy partner ecosystems.",
                rationale="A strong niche community can outperform broad paid acquisition early on.",
                expected_upside="Higher trust and warmer first-user cohorts.",
                priority="medium",
                tradeoffs=["Requires careful targeting.", "Community launches can underperform if the narrative is too broad."],
                next_actions=["Pick one niche community with clear pain overlap.", "Prepare a tailored launch post and onboarding path."],
            ),
        ],
        notes=[
            "Treat each experiment as a measurable draft, not a fixed strategy.",
            f"Failed slices to avoid over-claiming in growth copy: {failure_summary}.",
            "Use product-state memory to avoid repeating failed channel ideas.",
        ],
    )

    revenue = StrategySection(
        bot="revenue-bot",
        focus="pricing and monetization options",
        recommendation="Only price what the current implementation can reliably deliver; start high-touch if execution still needs operator help.",
        options=[
            StrategyOption(
                name="Concierge onboarding offer",
                summary=f"Sell {service_name} as a setup-assisted offer while the workflow for {slice_summary} is still being hardened.",
                rationale="High-touch revenue closes the learning loop on real value faster than waiting for a perfect self-serve funnel.",
                expected_upside="Gets to first revenue quickly and reveals the most valuable feature gaps.",
                priority="high",
                tradeoffs=["Less scalable.", "Operator time becomes part of the delivery cost."],
                next_actions=["Define one premium setup package.", "Write down the manual steps so they can be automated later."],
            ),
            StrategyOption(
                name="Tiered recurring plans",
                summary=f"Offer simple tiers based on supported slices ({slice_summary}) or number of active projects.",
                rationale="Tiering fits recurring operational products and gives a clear upgrade path.",
                expected_upside="Cleaner recurring revenue model and easier plan comparison.",
                priority="medium",
                tradeoffs=["Needs clear value boundaries.", "Poor tier design can create support burden."],
                next_actions=["Draft three plans with feature boundaries.", "Map each plan to a distinct customer profile."],
            ),
            StrategyOption(
                name="Team or usage-based expansion",
                summary="Charge more for collaboration, higher run volume, or advanced strategy/reporting workflows.",
                rationale="Usage or team expansion aligns revenue with actual operational value as adoption grows.",
                expected_upside="Better monetization for heavy users without blocking early adoption.",
                priority="medium",
                tradeoffs=["Harder to explain early.", "Requires reliable usage tracking and pricing communication."],
                next_actions=["Define one measurable expansion metric.", "Test willingness to pay with two early users before automating billing logic."],
            ),
        ],
        notes=[
            "Keep pricing decisions human-approved.",
            f"Do not price capabilities tied to failed slices: {failure_summary}.",
            "Use product-state memory to track which pricing hypotheses have already been tested.",
        ],
    )

    launch = StrategySection(
        bot="launch-bot",
        focus="launch sequencing and operational rollout",
        recommendation=launch_state,
        options=[
            StrategyOption(
                name="Quiet beta",
                summary=f"Launch to a small operator cohort, verify handoff quality, and tighten the setup path around {slice_summary} before broad promotion.",
                rationale="Lower risk and better for catching reliability issues before public distribution.",
                expected_upside="Better early product quality and cleaner messaging before a larger launch.",
                priority="high",
                tradeoffs=["Slower public momentum.", "Requires discipline to avoid staying in private beta too long."],
                next_actions=["Pick five beta users.", "Track onboarding friction and QA gaps from each run."],
            ),
            StrategyOption(
                name="Public build-in-public launch",
                summary=f"Share the product creation workflow, overnight results, and learning loop publicly once {proof_asset} is strong enough to support the claim.",
                rationale="The workflow itself is differentiated enough to become part of the marketing story.",
                expected_upside="Strong content loop and public feedback.",
                priority="medium",
                tradeoffs=["Public rough edges are visible.", "Requires consistency in updates and proof artifacts."],
                next_actions=["Prepare one narrative arc around a real product run.", "Publish the run summary and invite beta interest."],
            ),
            StrategyOption(
                name="Partner or community co-launch",
                summary="Bundle the launch with a trusted audience or ecosystem that already serves the target operator group.",
                rationale="Borrowed trust can improve first conversion rates.",
                expected_upside="Warmer traffic and easier social proof.",
                priority="medium",
                tradeoffs=["Needs partnership fit.", "Partner timeline can slow launch timing."],
                next_actions=["Identify one aligned community or partner.", "Tailor the launch message to their operator pain."],
            ),
        ],
        notes=[
            f"Current blocker for launch readiness: {top_blocker}.",
            f"Current execution proof: {slice_summary}.",
            "Do not treat strategy output as a substitute for QA or release approval.",
        ],
    )

    ops = StrategySection(
        bot="ops-bot",
        focus="operator coordination and next-step prioritization",
        recommendation="Keep GitHub as the source of truth, use local handoff for private operator review only, and gate every release through human QA plus approval.",
        options=[
            StrategyOption(
                name="QA-first release rhythm",
                summary="After each overnight build, verify the critical path, update blockers, and only then choose a strategy path to execute.",
                rationale="Reliable execution quality compounds faster than strategy experimentation on top of unstable output.",
                expected_upside="Fewer broken launches and better confidence in what to improve next.",
                priority="high",
                tradeoffs=["Can feel slower than pushing every run live.", "Needs a disciplined morning review habit."],
                next_actions=["Run the QA checklist before any public claim.", "Decide one growth and one pricing experiment after QA passes."],
            ),
            StrategyOption(
                name="Memory-backed operating cadence",
                summary="Use saved blockers, lessons, and next actions to drive the next run instead of starting from scratch.",
                rationale="Long-running systems improve when they preserve what failed, what worked, and what should happen next.",
                expected_upside="Better continuity across overnight runs and fewer repeated mistakes.",
                priority="high",
                tradeoffs=["Needs regular cleanup of stale lessons.", "Can become noisy without prioritization rules."],
                next_actions=["Review the latest lessons-learned set.", "Promote only the highest-signal lessons into the next plan."],
            ),
        ],
        notes=[
            "local handoff should remain a review artifact, not the canonical archive.",
            "external command channels are not part of the supported runtime surface.",
            "Self-improvement proposals must stay draft-only until a human approves them.",
        ],
    )

    return [positioning, growth, revenue, launch, ops]


def _lessons(plan: RunPlan, product_state: ProductState) -> list[MemoryNote]:
    notes: list[MemoryNote] = []
    for blocker in plan.blockers[:3]:
        notes.append(MemoryNote(kind="blocker", summary=blocker, priority="high", recommended_follow_up="Resolve before the next release decision."))
    for warning in plan.warnings[:3]:
        notes.append(MemoryNote(kind="warning", summary=warning, priority="medium", recommended_follow_up="Review during morning handoff triage."))
    if plan.platform_target == "multi-platform":
        notes.append(
            MemoryNote(
                kind="planning",
                summary="Multi-platform runs work better when the PRD resolves exact slices earlier.",
                priority="medium",
                recommended_follow_up="Add a platform-resolution checklist or helper before the next broad run.",
            )
        )
    notes.append(
        MemoryNote(
            kind="ops",
            summary=f"Current product stage is '{product_state.current_stage}' and should drive the next operator action.",
            priority="medium",
            recommended_follow_up="Use the stored next actions to choose one QA task and one business experiment.",
        )
    )
    return notes[:6]


def _self_improvement(plan: RunPlan, product_state: ProductState, lessons: list[MemoryNote]) -> list[SelfImprovementProposal]:
    proposals: list[SelfImprovementProposal] = []
    if plan.platform_target == "multi-platform":
        proposals.append(
            SelfImprovementProposal(
                title="Add stronger platform-resolution support",
                summary="Reduce ambiguity in multi-platform runs by preserving a reusable slice-resolution checklist or helper.",
                proposed_changes=[
                    "Add a runtime helper that turns PRD scope into explicit slice recommendations.",
                    "Store the chosen slice set in product-state memory for the next run.",
                ],
                reasons=["Multi-platform runs can stay too abstract without explicit slice decisions."],
            )
        )
    if any("missing" in note.summary.lower() or "credential" in note.summary.lower() for note in lessons):
        proposals.append(
            SelfImprovementProposal(
                title="Add credential preflight drafts",
                summary="Convert repeated secret or credential issues into a reusable preflight checklist draft.",
                proposed_changes=[
                    "Generate a preflight checklist section in the handoff when credentials are missing.",
                    "Store credential blockers as recurring lessons for future runs.",
                ],
                reasons=["Credential failures should become reusable operator guidance rather than repeated surprises."],
            )
        )
    proposals.append(
        SelfImprovementProposal(
            title="Draft strategy-review checklist",
            summary="Create a reusable checklist for reviewing positioning, growth, launch, and revenue options before acting on them.",
            proposed_changes=[
                "Add a strategy review checklist to the morning handoff template.",
                "Require product-state context before accepting growth or pricing recommendations.",
            ],
            reasons=["Strategy output should remain grounded in actual product state and operator review."],
        )
    )
    if product_state.current_stage in {"blocked", "partial-success"}:
        proposals.append(
            SelfImprovementProposal(
                title="Improve blocker-to-next-action mapping",
                summary="Turn top blockers into explicit next-run actions automatically.",
                proposed_changes=[
                    "Promote the highest-severity blocker into the default next action list.",
                    "Persist blocker categories so repeated failures can be deduplicated.",
                ],
                reasons=["Blocked runs should teach the next run what to fix first."],
            )
        )
    return proposals[:4]


def hydrate_plan_context(plan: RunPlan, sections: dict[str, str]) -> RunPlan:
    goal = _first_nonempty_line(sections.get("Goal", "")) or plan.title
    context_items = _bullet_lines(sections.get("Context", ""))
    acceptance = _bullet_lines(sections.get("Acceptance criteria", ""))
    handoff = _bullet_lines(sections.get("Human handoff", ""))
    title = plan.title.strip()
    service_slug = slugify(title)
    target_user = _infer_target_user(goal, context_items, title)
    problem = _infer_problem(goal, context_items, title)
    current_stage = _stage_for(plan)

    strategy_sections = _strategy_sections(title, goal, target_user, problem, plan)
    product_state = ProductState(
        service_slug=service_slug,
        title=title,
        product_goal=goal,
        target_user=target_user,
        problem_statement=problem,
        current_stage=current_stage,
        qa_risks=_pick(plan.blockers + plan.warnings, "Validate the critical user flow before release decisions."),
        blockers=list(plan.blockers),
        growth_experiments=[option.name for option in strategy_sections[1].options[:3]],
        pricing_hypotheses=[option.name for option in strategy_sections[2].options[:3]],
        launch_hypotheses=[option.name for option in strategy_sections[3].options[:3]],
        next_actions=_top_actions(plan, acceptance, handoff),
    )
    lessons = _lessons(plan, product_state)
    proposals = _self_improvement(plan, product_state, lessons)

    plan.product_state = product_state
    plan.strategy_sections = strategy_sections
    plan.lessons_learned = lessons
    plan.self_improvement_proposals = proposals
    return plan
