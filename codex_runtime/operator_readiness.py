from __future__ import annotations

import os
from pathlib import Path
import shutil
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def _check_http_service(name: str, base_url: str) -> dict:
    if not base_url:
        return {
            "name": name,
            "status": "not_configured",
            "base_url": "",
            "warning": f"{name} base URL is not configured.",
        }

    request = Request(base_url, method="GET")
    try:
        with urlopen(request, timeout=1.5) as response:
            return {
                "name": name,
                "status": "reachable",
                "base_url": base_url,
                "http_status": response.status,
            }
    except HTTPError as error:
        return {
            "name": name,
            "status": "reachable_with_http_error",
            "base_url": base_url,
            "http_status": error.code,
            "warning": f"{name} responded with HTTP {error.code}.",
        }
    except (URLError, TimeoutError, OSError) as error:
        return {
            "name": name,
            "status": "unreachable",
            "base_url": base_url,
            "warning": f"{name} is configured but not reachable: {error}",
        }


def _command_readiness(command: str) -> dict:
    path = shutil.which(command) if command else None
    return {
        "command": command,
        "available": bool(path),
        "path": path or "",
    }


def _path_readiness(path_value: str) -> dict:
    if not path_value:
        return {
            "path": "",
            "status": "not_configured",
            "exists": False,
        }
    path = Path(path_value).expanduser()
    return {
        "path": str(path),
        "status": "available" if path.exists() else "not_found",
        "exists": path.exists(),
    }


def _risk(identifier: str, severity: str, status: str, action: str) -> dict:
    return {
        "id": identifier,
        "severity": severity,
        "status": status,
        "action": action,
    }


def build_operator_readiness() -> dict:
    operator_platform = _env("CODEX_OPERATOR_PLATFORM", "paperclip")
    hermes_mode = _env("CODEX_HERMES_ADAPTER_MODE", "contract")
    hermes_command = _env("CODEX_HERMES_COMMAND", "hermes")
    memory_backend = _env("CODEX_MEMORY_BACKEND", "json")
    paperclip_base_url = _env("CODEX_PAPERCLIP_BASE_URL")
    paperclip_api_url = _env("CODEX_PAPERCLIP_API_URL")
    paperclip_hermes_agent_name = _env("CODEX_PAPERCLIP_HERMES_AGENT_NAME", "Hermes Engineer")
    graphiti_base_url = _env("CODEX_GRAPHITI_BASE_URL")
    graphiti_group_id = _env("CODEX_GRAPHITI_GROUP_ID")
    external_tools_mode = _env("CODEX_EXTERNAL_TOOLS_MODE", "off")
    understand_anything_mode = _env("CODEX_UNDERSTAND_ANYTHING_MODE", "off")
    understand_anything_path = _env("CODEX_UNDERSTAND_ANYTHING_PATH")
    taste_review_level = _env("CODEX_TASTE_REVIEW_LEVEL", "standard")
    copy_review_level = _env("CODEX_COPY_REVIEW_LEVEL", "standard")
    verification_loop_mode = _env("CODEX_VERIFICATION_LOOP_MODE", "contract")

    warnings: list[str] = []
    risks: list[dict] = []
    next_actions: list[str] = []

    local_tools = {
        "node": _command_readiness("node"),
        "npx": _command_readiness("npx"),
        "pnpm": _command_readiness("pnpm"),
    }
    if hermes_mode == "paperclip":
        if not local_tools["node"]["available"]:
            warnings.append("Paperclip local setup expects Node.js, but `node` is not available on PATH.")
            risks.append(_risk("paperclip-node", "medium", "open", "Install Node.js before running Paperclip locally."))
        if not local_tools["npx"]["available"] and not local_tools["pnpm"]["available"]:
            warnings.append("Paperclip local setup expects `npx` or `pnpm`, but neither command is available on PATH.")
            risks.append(_risk("paperclip-package-runner", "medium", "open", "Install npx or pnpm before running Paperclip locally."))

    paperclip_ui = _check_http_service("paperclip-ui", paperclip_base_url) if paperclip_base_url else {
        "name": "paperclip-ui",
        "status": "not_configured",
        "base_url": "",
        "warning": "paperclip-ui base URL is not configured.",
    }
    paperclip_api = _check_http_service("paperclip-api", paperclip_api_url) if paperclip_api_url else {
        "name": "paperclip-api",
        "status": "not_configured",
        "base_url": "",
        "warning": "paperclip-api URL is not configured.",
    }
    if hermes_mode == "paperclip" and paperclip_api.get("warning"):
        warnings.append(paperclip_api["warning"])
        risks.append(
            _risk(
                "paperclip-api",
                "medium",
                "open",
                "Start Paperclip locally and set CODEX_PAPERCLIP_API_URL, or keep using local Codex app mode.",
            )
        )

    if hermes_mode not in {"contract", "disabled", "local", "paperclip"}:
        warnings.append(f"Unsupported CODEX_HERMES_ADAPTER_MODE={hermes_mode!r}; expected contract, disabled, local, or paperclip.")
        risks.append(_risk("hermes-mode", "medium", "open", "Set CODEX_HERMES_ADAPTER_MODE to contract, disabled, local, or paperclip."))
    hermes_command_readiness = _command_readiness(hermes_command)
    provider_key_detected = any(
        bool(_env(name))
        for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY", "NOUS_API_KEY")
    )
    hermes = {
        "mode": hermes_mode,
        "status": "contract_only" if hermes_mode == "contract" else hermes_mode,
        "required_for_pr_validation": False,
        "secrets_policy": "local_or_self_hosted_only",
        "command": hermes_command_readiness,
        "provider_key_detected": provider_key_detected,
        "paperclip_adapter": {
            "package": "hermes-paperclip-adapter",
            "adapter_type": "hermes_local",
            "agent_name": paperclip_hermes_agent_name,
            "worktree_mode_recommended": True,
            "checkpoints_recommended": True,
        },
        "notes": [
            "Hermes execution is not required for GitHub Actions.",
            "Hermes execution remains opt-in for local or self-hosted workers.",
        ],
    }
    if hermes_mode in {"local", "paperclip"} and not hermes_command_readiness["available"]:
        warnings.append(f"CODEX_HERMES_ADAPTER_MODE={hermes_mode} but `{hermes_command}` is not available on PATH.")
        risks.append(_risk("hermes-command", "medium", "open", "Install Hermes locally or set CODEX_HERMES_COMMAND to the local Hermes binary."))
    if hermes_mode in {"local", "paperclip"} and not provider_key_detected:
        warnings.append("Hermes local execution usually needs a provider key injected outside tracked files.")
        risks.append(_risk("hermes-provider-key", "high", "open", "Inject a provider key locally or through a self-hosted runner secret store, never tracked files."))
    if hermes_mode == "paperclip" and not paperclip_api["status"].startswith("reachable"):
        warnings.append("CODEX_HERMES_ADAPTER_MODE=paperclip but Paperclip API is not reachable.")

    if memory_backend == "json":
        memory = {
            "backend": "json",
            "status": "ready",
            "required_for_pr_validation": True,
            "notes": ["Local JSON under codex_runtime_state remains the safe default."],
        }
    elif memory_backend == "graphiti":
        graphiti = _check_http_service("graphiti", graphiti_base_url)
        if not graphiti_group_id:
            warnings.append("CODEX_MEMORY_BACKEND=graphiti but CODEX_GRAPHITI_GROUP_ID is not configured.")
            risks.append(_risk("graphiti-group", "low", "open", "Set CODEX_GRAPHITI_GROUP_ID when enabling Graphiti memory."))
        if graphiti.get("warning"):
            warnings.append(graphiti["warning"])
            risks.append(_risk("graphiti-service", "medium", "open", "Start Graphiti with Neo4j or keep CODEX_MEMORY_BACKEND=json."))
        memory = {
            "backend": "graphiti",
            "status": "configured" if graphiti["status"].startswith("reachable") and graphiti_group_id else "not_configured",
            "required_for_pr_validation": False,
            "graphiti": {
                **graphiti,
                "group_id_configured": bool(graphiti_group_id),
                "neo4j_backend": "preferred",
            },
            "fallback_backend": "json",
        }
    else:
        warnings.append(f"Unsupported CODEX_MEMORY_BACKEND={memory_backend!r}; expected json or graphiti.")
        risks.append(_risk("memory-backend", "medium", "open", "Set CODEX_MEMORY_BACKEND to json or graphiti."))
        memory = {
            "backend": memory_backend,
            "status": "unsupported",
            "required_for_pr_validation": False,
            "fallback_backend": "json",
        }

    if operator_platform not in {"paperclip", "none"}:
        warnings.append(f"Unsupported CODEX_OPERATOR_PLATFORM={operator_platform!r}; expected paperclip or none.")
        risks.append(_risk("operator-platform", "low", "open", "Set CODEX_OPERATOR_PLATFORM to paperclip or none."))

    if external_tools_mode not in {"off", "opt-in"}:
        warnings.append(f"Unsupported CODEX_EXTERNAL_TOOLS_MODE={external_tools_mode!r}; expected off or opt-in.")
        risks.append(_risk("external-tools-mode", "low", "open", "Set CODEX_EXTERNAL_TOOLS_MODE to off or opt-in."))

    if understand_anything_mode not in {"off", "local", "committed-json"}:
        warnings.append(
            f"Unsupported CODEX_UNDERSTAND_ANYTHING_MODE={understand_anything_mode!r}; expected off, local, or committed-json."
        )
        risks.append(
            _risk(
                "understand-anything-mode",
                "low",
                "open",
                "Set CODEX_UNDERSTAND_ANYTHING_MODE to off, local, or committed-json.",
            )
        )

    understand_path = _path_readiness(understand_anything_path)
    understand_graph_path = Path(".understand-anything")
    if external_tools_mode == "opt-in" and understand_anything_mode == "local" and not understand_path["exists"]:
        warnings.append("Understand Anything local mode is enabled but CODEX_UNDERSTAND_ANYTHING_PATH is not configured or not found.")
        risks.append(
            _risk(
                "understand-anything-local-path",
                "low",
                "open",
                "Set CODEX_UNDERSTAND_ANYTHING_PATH to an approved local checkout or keep CODEX_UNDERSTAND_ANYTHING_MODE=off.",
            )
        )
    if external_tools_mode == "opt-in" and understand_anything_mode == "committed-json" and not understand_graph_path.exists():
        warnings.append("Understand Anything committed-json mode is enabled but .understand-anything is not present in this repo.")
        risks.append(
            _risk(
                "understand-anything-graph",
                "low",
                "open",
                "Commit sanitized graph JSON only after approval, or use CODEX_UNDERSTAND_ANYTHING_MODE=off.",
            )
        )
    if understand_anything_mode == "off":
        understand_status = "disabled"
    elif understand_anything_mode == "local":
        understand_status = "available" if understand_path["exists"] else "not_configured"
    elif understand_anything_mode == "committed-json":
        understand_status = "available" if understand_graph_path.exists() else "not_configured"
    else:
        understand_status = "unsupported"

    if taste_review_level not in {"standard", "strict"}:
        warnings.append(f"Unsupported CODEX_TASTE_REVIEW_LEVEL={taste_review_level!r}; expected standard or strict.")
        risks.append(_risk("taste-review-level", "low", "open", "Set CODEX_TASTE_REVIEW_LEVEL to standard or strict."))
    if copy_review_level not in {"standard", "strict"}:
        warnings.append(f"Unsupported CODEX_COPY_REVIEW_LEVEL={copy_review_level!r}; expected standard or strict.")
        risks.append(_risk("copy-review-level", "low", "open", "Set CODEX_COPY_REVIEW_LEVEL to standard or strict."))
    if verification_loop_mode not in {"contract", "local"}:
        warnings.append(f"Unsupported CODEX_VERIFICATION_LOOP_MODE={verification_loop_mode!r}; expected contract or local.")
        risks.append(_risk("verification-loop-mode", "low", "open", "Set CODEX_VERIFICATION_LOOP_MODE to contract or local."))

    external_tools = {
        "mode": external_tools_mode,
        "required_for_pr_validation": False,
        "default_dependency_policy": "no_external_installs",
        "knowledge_work_plugins": {
            "status": "pattern_adopted",
            "required_for_pr_validation": False,
            "local_contract": "docs/role-plugin-operating-model.md",
        },
        "understand_anything": {
            "mode": understand_anything_mode,
            "status": understand_status,
            "required_for_pr_validation": False,
            "path": understand_path,
            "committed_graph": {
                "path": str(understand_graph_path),
                "exists": understand_graph_path.exists(),
                "status": "available" if understand_graph_path.exists() else "not_configured",
            },
            "contract": "docs/codebase-knowledge-graph-contract.md",
        },
        "taste_review": {
            "level": taste_review_level,
            "status": "ready" if taste_review_level in {"standard", "strict"} else "unsupported",
            "agent": ".codex/agents/senior_product_designer.toml",
            "skill": ".agents/skills/frontend-taste-review/SKILL.md",
            "contract": "docs/taste-and-copy-quality-contract.md",
        },
        "copy_review": {
            "level": copy_review_level,
            "status": "ready" if copy_review_level in {"standard", "strict"} else "unsupported",
            "agent": ".codex/agents/copy_quality_reviewer.toml",
            "skill": ".agents/skills/anti-slop-copy-review/SKILL.md",
            "contract": "docs/taste-and-copy-quality-contract.md",
        },
        "verification_loop": {
            "mode": verification_loop_mode,
            "status": "contract_ready" if verification_loop_mode == "contract" else "local_optional",
            "required_for_pr_validation": False,
            "agent": ".codex/agents/verification_loop_specialist.toml",
            "skill": ".agents/skills/verification-loop/SKILL.md",
            "contract": "docs/verification-loop-contract.md",
            "local_harness": {
                "status": "not_configured",
                "required_for_pr_validation": False,
            },
        },
    }

    if hermes_mode == "contract":
        next_actions.append("Use local Codex app as the primary worker; Paperclip/Hermes remains a documented optional path.")
    if hermes_mode == "paperclip":
        next_actions.append("Run Paperclip outside this repository, set CODEX_PAPERCLIP_API_URL, install Hermes, then rerun readiness.")
    if memory_backend == "json":
        next_actions.append("Keep local JSON memory as the default until Graphiti is intentionally enabled.")
    if memory_backend == "graphiti":
        next_actions.append("Start Graphiti with Neo4j and set CODEX_GRAPHITI_BASE_URL plus CODEX_GRAPHITI_GROUP_ID.")
    next_actions.append("Use service basecamp contracts before scaffolding any new web/app service.")
    next_actions.append("Use the senior design layer before accepting UI-heavy work.")
    next_actions.append("Use external pattern tools only through the opt-in runbook and human-approved local setup.")

    return {
        "operator_readiness_version": 1,
        "status": "ready" if not risks else "needs_optional_setup",
        "goal_contract": {
            "command": "/goal",
            "status": "ready",
            "required_fields": [
                "goal",
                "product",
                "success_criteria",
                "target_platforms",
                "constraints",
                "validation_commands",
                "approval_boundary",
            ],
            "default_flow": "Turn /goal into a PRD, implement with local Codex app, validate through GitHub Actions, then update memory.",
        },
        "service_basecamp": {
            "status": "contract_ready",
            "required_for_pr_validation": False,
            "template_scaffolded": False,
            "monthly_vps_budget_krw_max": 100000,
            "default_service_type": "web_saas",
            "default_stack": {
                "web": "Next.js App Router",
                "language": "TypeScript",
                "package_manager": "pnpm",
                "ui": "Tailwind CSS plus shadcn/ui-compatible components",
                "database": "PostgreSQL",
                "orm": "Drizzle",
                "auth": "Auth.js-compatible server-owned session boundary",
                "billing": "Stripe-first provider adapter with Toss Payments extension path",
                "deployment": "single VPS with Docker Compose and Caddy",
            },
            "required_contracts": [
                "docs/service-basecamp-architecture.md",
                "docs/service-template-contract.md",
                "docs/hermes-service-factory-contract.md",
                "docs/vps-deployment-contract.md",
                "docs/revenue-system-contract.md",
                "docs/admin-observability-contract.md",
            ],
            "safety_boundaries": [
                "No tracked secrets.",
                "No live auth, payment, or deployment changes in the basecamp contract phase.",
                "No production deployment or protected-branch merge by Hermes.",
                "No optional service required for GitHub Actions validation.",
            ],
            "next_phase": "Create a separate web-saas product template scaffold only after approval.",
        },
        "design_layer": {
            "status": "contract_ready",
            "required_for_pr_validation": False,
            "visual_qa_tooling_installed": False,
            "default_taste_anchor": "Midday",
            "reference_anchors": ["Midday", "Dub", "PostHog", "Twenty", "Huly"],
            "required_contracts": [
                "docs/DESIGN.md",
                "docs/design-reference-library.md",
                "docs/design-system-contract.md",
                "docs/senior-designer-review-checklist.md",
                "docs/visual-qa-contract.md",
            ],
            "agent": ".codex/agents/senior_product_designer.toml",
            "safety_boundaries": [
                "References are inspiration only; do not copy code, assets, logos, or exact layouts.",
                "No Storybook, Chromatic, Figma, or visual SaaS dependency is required in this phase.",
                "UI-heavy work should include senior designer review and screenshot evidence when a runnable UI exists.",
            ],
        },
        "external_tools": external_tools,
        "agent_army": {
            "status": "ready",
            "required_for_pr_validation": False,
            "routing_command": "python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty",
            "supported_service_types": [
                "web_saas",
                "subscription_credit_saas",
                "marketplace",
                "mobile_app",
                "ai_agent_service",
                "data_dashboard",
                "finance_sensitive",
                "consumer_content_app",
            ],
            "supported_phases": [
                "discovery",
                "prd",
                "ux",
                "architecture",
                "implementation",
                "qa",
                "release",
                "growth",
            ],
            "contracts": [
                "docs/agent-army-operating-model.md",
                "docs/service-agent-routing-matrix.md",
                "docs/agent-team-presets.md",
                "docs/agent-copyright-attribution.md",
            ],
            "source_policy": "source_attributed_rewritten_roles",
        },
        "operator_platform": {
            "selected": operator_platform,
            "status": "paperclip_contract" if operator_platform == "paperclip" else "disabled",
            "required_for_pr_validation": False,
            "local_tools": local_tools,
            "paperclip": {
                "ui": paperclip_ui,
                "api": paperclip_api,
                "default_local_api_url": "http://127.0.0.1:3100/api",
            },
        },
        "hermes_adapter": hermes,
        "memory": memory,
        "github_actions": {
            "api_key_free": True,
            "ai_review_or_fix_jobs_enabled": False,
            "required_ai_services": [],
        },
        "warnings": warnings,
        "risks": risks,
        "next_actions": next_actions,
        "blockers": [],
    }
