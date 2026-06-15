from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class PlatformSlice:
    platform: str
    builders: list[str]
    validation_hint: str


@dataclass
class AuthStatus:
    github_mode: str
    github_ready: bool
    provider_ready: bool


@dataclass
class DeliveryStatus:
    requested_mode: str
    protected_branch_safe_default: bool = True
    direct_protected_push_allowed: bool = False
    can_attempt_repo_create: bool = False
    can_attempt_branch_delivery: bool = False


@dataclass
class ReportingStatus:
    requested_mode: str
    github_summary_required: bool = True


@dataclass
class BuilderSliceExecution:
    platform: str
    builders: list[str]
    command: list[str] = field(default_factory=list)
    log_path: str = ""
    executed: bool = False
    success: bool = False
    return_code: int | None = None
    notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class GitHubDeliveryPlan:
    cwd: str
    repository_owner: str
    repository_name: str
    remote_name: str
    base_branch: str
    branch_name: str
    commit_message: str
    pr_title: str
    pr_body_path: str
    requested_mode: str
    live_mode: bool
    repo_create_requested: bool = False
    branch_delivery_requested: bool = False
    draft_pr_requested: bool = False
    commands: list[list[str]] = field(default_factory=list)
    executed_commands: list[list[str]] = field(default_factory=list)
    skipped_commands: list[list[str]] = field(default_factory=list)
    head_sha: str = ""
    repository_url: str = ""
    pr_url: str = ""
    notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class ReportingDispatch:
    requested_mode: str
    live_mode: bool
    handoff_path: str
    summary_text: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class StrategyOption:
    name: str
    summary: str
    rationale: str
    expected_upside: str
    priority: str = "medium"
    tradeoffs: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)


@dataclass
class StrategySection:
    bot: str
    focus: str
    recommendation: str
    options: list[StrategyOption] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class ProductState:
    service_slug: str
    title: str
    product_goal: str
    target_user: str
    problem_statement: str
    current_stage: str
    qa_risks: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    growth_experiments: list[str] = field(default_factory=list)
    pricing_hypotheses: list[str] = field(default_factory=list)
    launch_hypotheses: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)


@dataclass
class MemoryNote:
    kind: str
    summary: str
    priority: str = "medium"
    recommended_follow_up: str = ""


@dataclass
class SelfImprovementProposal:
    title: str
    summary: str
    proposed_changes: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    review_required: bool = True
    status: str = "draft"


@dataclass
class RunPlan:
    prd_path: str
    title: str
    platform_target: str
    delivery_mode: str
    reporting_mode: str
    supported: bool
    slices: list[PlatformSlice] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    auth: AuthStatus | None = None
    delivery: DeliveryStatus | None = None
    reporting: ReportingStatus | None = None
    builder_execution: list[BuilderSliceExecution] = field(default_factory=list)
    github_delivery: GitHubDeliveryPlan | None = None
    reporting_dispatch: ReportingDispatch | None = None
    product_state: ProductState | None = None
    strategy_sections: list[StrategySection] = field(default_factory=list)
    lessons_learned: list[MemoryNote] = field(default_factory=list)
    self_improvement_proposals: list[SelfImprovementProposal] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
