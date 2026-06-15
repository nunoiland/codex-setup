from __future__ import annotations

from copy import deepcopy


SUPPORTED_SERVICE_TYPES = {
    "web_saas",
    "subscription_credit_saas",
    "marketplace",
    "mobile_app",
    "ai_agent_service",
    "data_dashboard",
    "finance_sensitive",
    "consumer_content_app",
}

SUPPORTED_PHASES = {
    "discovery",
    "prd",
    "ux",
    "architecture",
    "implementation",
    "qa",
    "release",
    "growth",
}


PHASE_BASELINES: dict[str, dict[str, list[str]]] = {
    "discovery": {
        "primary_agents": ["product_manager", "business_analyst", "market_researcher"],
        "reviewer_agents": ["prd_orchestrator", "copy_quality_reviewer"],
        "optional_agents": ["competitive_intelligence", "business_model_strategist"],
        "validation_gates": [
            "Problem, target user, success criteria, and constraints are explicit.",
            "Known assumptions are separated from verified facts.",
        ],
        "risks": [
            "Generic market claims can hide weak product focus.",
            "Discovery output is draft strategy until human-reviewed.",
        ],
    },
    "prd": {
        "primary_agents": ["product_manager", "prd_orchestrator", "story_delivery_manager"],
        "reviewer_agents": ["qa_reviewer", "security_reviewer", "technical_writer"],
        "optional_agents": ["business_analyst", "copy_quality_reviewer"],
        "validation_gates": [
            "PRD includes platform target, success criteria, constraints, validation commands, and approval boundaries.",
            "Medium or large work has a plan in PLANS/ before implementation.",
        ],
        "risks": [
            "Vague PRDs produce unfocused agent routing.",
            "Auth, payment, deployment, and secrets require explicit approval.",
        ],
    },
    "ux": {
        "primary_agents": ["ux_researcher", "ux_architect", "senior_product_designer"],
        "reviewer_agents": ["frontend_ux_engineer", "copy_quality_reviewer", "brand_guardian"],
        "optional_agents": ["product_ux_specialist", "ui_specialist"],
        "validation_gates": [
            "Core flows include loading, empty, error, permission, and edge states.",
            "UI-heavy work has design review and screenshot or visual QA evidence when runnable.",
        ],
        "risks": [
            "Attractive UI can still fail if flow or copy is unclear.",
            "Do not copy reference product layouts, assets, logos, or exact brand language.",
        ],
    },
    "architecture": {
        "primary_agents": ["solution_architect", "backend_reliability_engineer", "data_model_specialist"],
        "reviewer_agents": ["security_reviewer", "devops_sre_specialist", "database_optimizer"],
        "optional_agents": ["payment_auth_specialist", "ai_integration_engineer", "observability_specialist"],
        "validation_gates": [
            "System boundaries, data flow, integration points, and failure modes are documented.",
            "Risky auth, payment, database, deployment, and secrets work is approval-gated.",
        ],
        "risks": [
            "Overbuilt architecture slows MVP delivery.",
            "Hidden deployment or provider assumptions can create unsafe defaults.",
        ],
    },
    "implementation": {
        "primary_agents": ["web_builder", "api_builder", "frontend_ux_engineer"],
        "reviewer_agents": ["qa_reviewer", "security_reviewer", "performance_specialist"],
        "optional_agents": ["backend_reliability_engineer", "database_optimizer", "ai_integration_engineer"],
        "validation_gates": [
            "Implementation follows the approved plan and smallest effective diff.",
            "Relevant lint, typecheck, tests, build, and user-flow checks are run or marked unavailable with reason.",
        ],
        "risks": [
            "Builder agents must not edit outside assigned scope.",
            "Do not add dependencies or risky integrations without approval.",
        ],
    },
    "qa": {
        "primary_agents": ["qa_reviewer", "test_architect", "api_tester"],
        "reviewer_agents": ["verification_loop_specialist", "security_reviewer", "performance_specialist"],
        "optional_agents": ["observability_specialist", "frontend_ux_engineer"],
        "validation_gates": [
            "Failures include reproduction commands, logs, likely cause, and regression candidates.",
            "Security and secret boundaries are reviewed before completion.",
        ],
        "risks": [
            "Passing unit checks can miss broken user flows.",
            "Skipped validation must be reported honestly.",
        ],
    },
    "release": {
        "primary_agents": ["release_specialist", "devops_sre_specialist", "observability_specialist"],
        "reviewer_agents": ["security_reviewer", "compliance_risk_reviewer", "qa_reviewer"],
        "optional_agents": ["customer_success_reviewer", "technical_writer"],
        "validation_gates": [
            "Release notes, rollback path, monitoring, and known risks are documented.",
            "No production deployment or protected-branch mutation happens without explicit approval.",
        ],
        "risks": [
            "Non-blocking security evidence still needs human review.",
            "Operational gaps can become expensive after launch.",
        ],
    },
    "growth": {
        "primary_agents": ["growth_marketer", "pricing_revenue_strategist", "customer_success_reviewer"],
        "reviewer_agents": ["copy_quality_reviewer", "brand_guardian", "product_manager"],
        "optional_agents": ["competitive_intelligence", "sales_strategy_reviewer", "app_store_optimizer"],
        "validation_gates": [
            "Growth experiments have a metric, hypothesis, target segment, and safe rollback.",
            "Pricing and revenue claims are reviewed as drafts before use.",
        ],
        "risks": [
            "Growth work can degrade trust if copy is exaggerated.",
            "Revenue strategy must not bypass billing, privacy, or compliance review.",
        ],
    },
}


SERVICE_OVERLAYS: dict[str, dict[str, list[str]]] = {
    "web_saas": {
        "primary_agents": [],
        "reviewer_agents": ["senior_product_designer", "security_reviewer"],
        "optional_agents": ["web_builder", "backend_reliability_engineer"],
        "validation_gates": ["Run web lint, typecheck, build, and health smoke when applicable."],
        "risks": ["SaaS defaults must include clear empty, error, admin, and health states."],
    },
    "subscription_credit_saas": {
        "primary_agents": ["payment_auth_specialist", "pricing_revenue_strategist"],
        "reviewer_agents": ["security_reviewer", "compliance_risk_reviewer"],
        "optional_agents": ["business_model_strategist", "observability_specialist"],
        "validation_gates": ["Billing, credits, auth, and usage limits require explicit human approval before live wiring."],
        "risks": ["Money-related logic has higher trust, legal, and support risk."],
    },
    "marketplace": {
        "primary_agents": ["business_model_strategist", "ux_architect"],
        "reviewer_agents": ["compliance_risk_reviewer", "customer_success_reviewer"],
        "optional_agents": ["payment_auth_specialist", "competitive_intelligence"],
        "validation_gates": ["Trust, dispute, seller/buyer state, and payout assumptions are documented."],
        "risks": ["Multi-sided workflows can hide permission, payout, and abuse edge cases."],
    },
    "mobile_app": {
        "primary_agents": ["android_builder", "ios_builder", "app_store_optimizer"],
        "reviewer_agents": ["ux_researcher", "performance_specialist"],
        "optional_agents": ["api_builder", "senior_product_designer"],
        "validation_gates": ["Mobile validation is reported per platform; missing native tooling is a blocker, not a pass."],
        "risks": ["Android and iOS drift if platform-specific checks are not separated."],
    },
    "ai_agent_service": {
        "primary_agents": ["ai_integration_engineer", "solution_architect"],
        "reviewer_agents": ["security_reviewer", "observability_specialist"],
        "optional_agents": ["verification_loop_specialist", "backend_reliability_engineer"],
        "validation_gates": ["AI behavior has explicit tool boundaries, eval ideas, cost controls, and secret boundaries."],
        "risks": ["Agent services can create hidden cost, privacy, and tool-permission risks."],
    },
    "data_dashboard": {
        "primary_agents": ["data_model_specialist", "database_optimizer"],
        "reviewer_agents": ["observability_specialist", "backend_reliability_engineer"],
        "optional_agents": ["frontend_ux_engineer", "api_tester"],
        "validation_gates": ["Metrics, dimensions, freshness, and query cost assumptions are explicit."],
        "risks": ["Dashboards can mislead if metric definitions or data freshness are unclear."],
    },
    "finance_sensitive": {
        "primary_agents": ["compliance_risk_reviewer", "security_reviewer", "business_analyst"],
        "reviewer_agents": ["copy_quality_reviewer", "data_model_specialist"],
        "optional_agents": ["pricing_revenue_strategist", "observability_specialist"],
        "validation_gates": ["Financial, investment-adjacent, billing, and privacy copy is conservative and reviewed."],
        "risks": ["Avoid guarantees, exaggerated claims, or unsupported financial advice."],
    },
    "consumer_content_app": {
        "primary_agents": ["brand_guardian", "growth_marketer", "ux_researcher"],
        "reviewer_agents": ["copy_quality_reviewer", "senior_product_designer"],
        "optional_agents": ["app_store_optimizer", "customer_success_reviewer"],
        "validation_gates": ["Content, community, moderation, and retention assumptions are explicit."],
        "risks": ["Consumer products need clear tone, moderation, and retention strategy to avoid low-quality growth."],
    },
}


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _agent(name: str, reason: str) -> dict:
    return {
        "name": name,
        "config": f".codex/agents/{name}.toml",
        "reason": reason,
    }


def _agent_list(names: list[str], phase: str, service_type: str, bucket: str) -> list[dict]:
    reason = {
        "primary_agents": f"Primary for {service_type} during {phase}.",
        "reviewer_agents": f"Review gate for {service_type} during {phase}.",
        "optional_agents": f"Add only if the PRD or plan needs this specialty.",
    }[bucket]
    return [_agent(name, reason) for name in names]


def recommend_agents(service_type: str, phase: str) -> dict:
    if service_type not in SUPPORTED_SERVICE_TYPES:
        raise ValueError(f"Unsupported service_type={service_type!r}. Supported: {', '.join(sorted(SUPPORTED_SERVICE_TYPES))}.")
    if phase not in SUPPORTED_PHASES:
        raise ValueError(f"Unsupported phase={phase!r}. Supported: {', '.join(sorted(SUPPORTED_PHASES))}.")

    baseline = deepcopy(PHASE_BASELINES[phase])
    overlay = SERVICE_OVERLAYS[service_type]
    merged = {
        "primary_agents": _dedupe(baseline["primary_agents"] + overlay["primary_agents"]),
        "reviewer_agents": _dedupe(baseline["reviewer_agents"] + overlay["reviewer_agents"]),
        "optional_agents": _dedupe(baseline["optional_agents"] + overlay["optional_agents"]),
        "validation_gates": _dedupe(baseline["validation_gates"] + overlay["validation_gates"]),
        "risks": _dedupe(baseline["risks"] + overlay["risks"]),
    }
    primary_set = set(merged["primary_agents"])
    merged["reviewer_agents"] = [name for name in merged["reviewer_agents"] if name not in primary_set]
    reviewer_set = set(merged["reviewer_agents"])
    merged["optional_agents"] = [
        name for name in merged["optional_agents"] if name not in primary_set and name not in reviewer_set
    ]

    return {
        "agent_recommendation_version": 1,
        "service_type": service_type,
        "phase": phase,
        "primary_agents": _agent_list(merged["primary_agents"], phase, service_type, "primary_agents"),
        "reviewer_agents": _agent_list(merged["reviewer_agents"], phase, service_type, "reviewer_agents"),
        "optional_agents": _agent_list(merged["optional_agents"], phase, service_type, "optional_agents"),
        "validation_gates": merged["validation_gates"],
        "risks": merged["risks"],
        "source_contracts": [
            "docs/agent-army-operating-model.md",
            "docs/service-agent-routing-matrix.md",
            "docs/agent-team-presets.md",
            "docs/agent-copyright-attribution.md",
        ],
        "safety_boundaries": [
            "PRD-first and plan-first remain mandatory for medium or large work.",
            "External agent repositories are pattern references only; local roles are rewritten.",
            "No external agent framework, API key, or secret is required for this recommendation.",
            "Auth, payment, secrets, deployment, dependencies, and destructive actions still require approval.",
        ],
    }
