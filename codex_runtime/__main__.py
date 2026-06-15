from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from .agent_routing import recommend_agents
from .builders import execute_builder_execution, prepare_builder_execution
from .github_delivery import execute_github_delivery, prepare_github_delivery
from .operator_readiness import build_operator_readiness
from .reporting import prepare_reporting
from .runner import build_run_plan, load_prd_sections
from .state import (
    list_product_states,
    list_queue_entries,
    list_run_records,
    load_improvement_proposals,
    load_product_state,
    load_queue_entry,
    load_run_record,
    next_queued_entry,
    save_improvement_proposals,
    save_product_state,
    save_queue_entry,
    save_run_record,
    schedule_for_delay,
    update_queue_entry,
)
from .strategy import hydrate_plan_context


EXECUTION_KEYS = (
    "prepare_builders",
    "execute_builders",
    "prepare_github_delivery",
    "execute_github_delivery",
    "prepare_reporting",
)


def _bool_request(args: argparse.Namespace, request: dict, name: str) -> bool:
    return bool(getattr(args, name) or request.get(name, False))


def _build_execution_request(args: argparse.Namespace) -> dict:
    scheduled_for = args.scheduled_for or (schedule_for_delay(args.schedule_delay_seconds) if args.schedule_delay_seconds else "")
    return {
        "cwd": str(Path(args.cwd).resolve()),
        "prepare_builders": bool(args.prepare_builders),
        "execute_builders": bool(args.execute_builders),
        "prepare_github_delivery": bool(args.prepare_github_delivery),
        "execute_github_delivery": bool(args.execute_github_delivery),
        "prepare_reporting": bool(args.prepare_reporting),
        "scheduled_for": scheduled_for,
        "retry_limit": args.retry_limit,
    }


def _resolve_resume_source(root: str | Path, run_id: str) -> tuple[dict, str]:
    try:
        return load_queue_entry(root, run_id), "queue"
    except FileNotFoundError:
        return load_run_record(root, run_id), "run"


def _status_for(plan) -> str:
    builders = plan.builder_execution
    delivery = plan.github_delivery
    reporting = plan.reporting_dispatch
    if plan.blockers:
        return "blocked"
    if builders and any(item.errors for item in builders):
        return "partial-success" if any(item.success for item in builders) else "failed"
    if delivery and delivery.errors:
        return "partial-success" if delivery.executed_commands else "failed"
    if reporting and reporting.errors:
        return "partial-success"
    if plan.warnings or (delivery and delivery.warnings) or (reporting and reporting.warnings) or any(
        item.warnings for item in builders
    ):
        return "partial-success"
    return "success"


def _record_payload(plan, execution_request: dict, cwd: str, *, status: str, lineage: dict | None = None) -> dict:
    payload = plan.to_dict()
    payload.update(
        {
            "cwd": str(Path(cwd).resolve()),
            "run_status": status,
            "execution_request": execution_request,
            "scheduled_for": execution_request.get("scheduled_for", ""),
            "retry_limit": execution_request.get("retry_limit", 1),
        }
    )
    if lineage:
        payload.update(lineage)
    if lineage and lineage.get("run_id"):
        payload["run_id"] = lineage["run_id"]
    payload.setdefault("retry_count", 0)
    return payload


def _record_and_print(payload: dict, pretty: bool) -> None:
    print(json.dumps(payload, indent=2 if pretty else None, ensure_ascii=False))


def _apply_execution(plan, cwd: str, execution_request: dict):
    if execution_request.get("prepare_builders") or execution_request.get("execute_builders"):
        builders = prepare_builder_execution(plan, Path(cwd), live_mode=execution_request.get("execute_builders", False))
        if execution_request.get("execute_builders"):
            builders = execute_builder_execution(plan, Path(cwd), builders)
        plan.builder_execution = builders

    if execution_request.get("prepare_github_delivery") or execution_request.get("execute_github_delivery"):
        delivery = prepare_github_delivery(plan, Path(cwd), live_mode=execution_request.get("execute_github_delivery", False))
        if execution_request.get("execute_github_delivery"):
            delivery = execute_github_delivery(delivery)
        plan.github_delivery = delivery

    if execution_request.get("prepare_reporting"):
        plan.reporting_dispatch = prepare_reporting(plan, Path(cwd), live_mode=False)

    _, sections = load_prd_sections(plan.prd_path)
    return hydrate_plan_context(plan, sections)


def _persist_artifacts(root: str | Path, payload: dict) -> dict:
    product_state = payload.get("product_state")
    if product_state:
        payload["product_state_path"] = save_product_state(
            root,
            product_state["service_slug"],
            {
                "run_id": payload.get("run_id"),
                **product_state,
            },
        )
    proposals = payload.get("self_improvement_proposals") or []
    run_id = payload.get("run_id")
    if run_id and proposals:
        payload["improvement_path"] = save_improvement_proposals(
            root,
            run_id,
            {
                "run_id": run_id,
                "title": payload.get("title"),
                "product_state": product_state,
                "self_improvement_proposals": proposals,
            },
        )
    payload["run_record_path"] = save_run_record(root, payload)
    return payload


def _retry_allowed(source_record: dict) -> tuple[bool, str]:
    retry_count = int(source_record.get("retry_count") or 0)
    retry_limit = int(source_record.get("retry_limit") or 1)
    if retry_limit >= 0 and retry_count >= retry_limit:
        return False, f"Retry limit reached for {source_record.get('run_id', 'run')} ({retry_count}/{retry_limit})."
    return True, ""


def _execution_request_from_source(args: argparse.Namespace, request: dict, source_record: dict) -> dict:
    execution_request = {key: _bool_request(args, request, key) for key in EXECUTION_KEYS}
    execution_request["scheduled_for"] = request.get("scheduled_for", "")
    execution_request["retry_limit"] = request.get("retry_limit", source_record.get("retry_limit", 1))
    return execution_request


def _execute_once(args: argparse.Namespace) -> dict:
    if args.recommend_agents:
        if not args.service_type or not args.phase:
            raise SystemExit("Provide --service-type and --phase with --recommend-agents.")
        try:
            return recommend_agents(args.service_type, args.phase)
        except ValueError as error:
            raise SystemExit(str(error)) from error

    if args.operator_readiness:
        return build_operator_readiness()

    if args.list_runs:
        return {
            "runs": list_run_records(args.cwd),
            "queue": list_queue_entries(args.cwd),
            "products": list_product_states(args.cwd),
        }

    if args.show_run:
        return load_run_record(args.cwd, args.show_run)

    if args.show_queue:
        return load_queue_entry(args.cwd, args.show_queue)

    if args.show_product_state:
        return load_product_state(args.cwd, args.show_product_state)

    if args.show_improvement_proposals:
        return load_improvement_proposals(args.cwd, args.show_improvement_proposals)

    source_record: dict | None = None
    source_kind = ""
    execution_request = _build_execution_request(args)
    lineage: dict | None = None

    if args.run_next_queued:
        source_record = next_queued_entry(args.cwd)
        if not source_record:
            return {"queue_status": "empty"}
        args.resume_run = source_record["run_id"]

    if args.resume_run:
        source_record, source_kind = _resolve_resume_source(args.cwd, args.resume_run)
        args.prd = source_record["prd_path"]
        args.cwd = source_record.get("cwd", args.cwd)
        execution_request = _execution_request_from_source(args, source_record.get("execution_request", {}), source_record)
        lineage = {
            "run_id": args.resume_run,
            "resumed_from": args.resume_run,
            "resume_source": source_kind,
            "retry_count": source_record.get("retry_count", 0),
        }
    elif args.retry_run:
        source_record = load_run_record(args.cwd, args.retry_run)
        allowed, message = _retry_allowed(source_record)
        if not allowed:
            return {"run_id": args.retry_run, "run_status": "blocked", "blockers": [message]}
        args.prd = source_record["prd_path"]
        args.cwd = source_record.get("cwd", args.cwd)
        execution_request = _execution_request_from_source(args, source_record.get("execution_request", {}), source_record)
        lineage = {"retry_of": args.retry_run, "retry_count": int(source_record.get("retry_count") or 0) + 1}

    if not args.prd:
        raise SystemExit(
            "Provide --prd, --resume-run, --retry-run, --list-runs, --show-run, --show-queue, --show-product-state, --show-improvement-proposals, --operator-readiness, --recommend-agents, or worker mode."
        )

    plan = build_run_plan(args.prd)
    payload = plan.to_dict()

    if args.queue_run:
        queue_payload = _record_payload(plan, execution_request, args.cwd, status="queued", lineage=lineage)
        queue_payload["queue_path"] = save_queue_entry(args.cwd, queue_payload)
        payload = _persist_artifacts(args.cwd, queue_payload)
        return payload

    if args.resume_run and source_kind == "queue":
        update_queue_entry(args.cwd, args.resume_run, {"queue_status": "running", "run_status": "running"})
    plan = _apply_execution(plan, args.cwd, execution_request)
    run_status = _status_for(plan)
    payload = _record_payload(plan, execution_request, args.cwd, status=run_status, lineage=lineage)
    payload = _persist_artifacts(args.cwd, payload)
    if args.resume_run and source_kind == "queue":
        payload["queue_path"] = update_queue_entry(
            args.cwd,
            args.resume_run,
            {"queue_status": run_status, "run_status": run_status},
        )
    return payload


def _worker_loop(args: argparse.Namespace) -> dict:
    runs_processed = 0
    idle_cycles = 0
    results: list[dict] = []
    while True:
        loop_args = argparse.Namespace(**vars(args))
        loop_args.run_next_queued = True
        loop_args.resume_run = None
        loop_args.retry_run = None
        loop_args.queue_run = False
        payload = _execute_once(loop_args)
        if payload.get("queue_status") == "empty":
            idle_cycles += 1
            if args.max_idle_cycles is not None and idle_cycles >= args.max_idle_cycles:
                return {
                    "worker_status": "idle_exit",
                    "runs_processed": runs_processed,
                    "idle_cycles": idle_cycles,
                    "results": results,
                }
            time.sleep(args.poll_seconds)
            continue

        idle_cycles = 0
        runs_processed += 1
        results.append(payload)
        if args.max_runs is not None and runs_processed >= args.max_runs:
            return {
                "worker_status": "max_runs_exit",
                "runs_processed": runs_processed,
                "idle_cycles": idle_cycles,
                "results": results,
            }


def main() -> None:
    parser = argparse.ArgumentParser(description="Codex-setting orchestration runtime.")
    parser.add_argument("--prd", help="Path to the product PRD markdown file.")
    parser.add_argument("--cwd", default=".", help="Repository cwd for delivery planning or execution.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON output.")
    parser.add_argument("--prepare-builders", action="store_true", help="Prepare platform-slice builder commands from env.")
    parser.add_argument("--execute-builders", action="store_true", help="Execute configured platform-slice builder commands when explicitly enabled via env.")
    parser.add_argument("--prepare-github-delivery", action="store_true", help="Add live GitHub delivery planning metadata.")
    parser.add_argument("--execute-github-delivery", action="store_true", help="Execute the prepared GitHub delivery commands when explicitly enabled via env.")
    parser.add_argument("--prepare-reporting", action="store_true", help="Render a GitHub-first local handoff artifact.")
    parser.add_argument("--queue-run", action="store_true", help="Queue the requested run instead of executing it now.")
    parser.add_argument("--resume-run", help="Resume a queued or recorded run by id.")
    parser.add_argument("--retry-run", help="Retry a previously recorded run by id.")
    parser.add_argument("--list-runs", action="store_true", help="List recorded runs, queue entries, and product states.")
    parser.add_argument("--show-run", help="Show a recorded run by id.")
    parser.add_argument("--show-queue", help="Show a queued run entry by id.")
    parser.add_argument("--show-product-state", help="Show a stored product-state snapshot by slug.")
    parser.add_argument("--show-improvement-proposals", help="Show stored self-improvement proposals by run id.")
    parser.add_argument("--operator-readiness", action="store_true", help="Report optional Product Factory operator, Hermes, and memory backend readiness.")
    parser.add_argument("--recommend-agents", action="store_true", help="Recommend an Agent Army team for a service type and lifecycle phase.")
    parser.add_argument("--service-type", help="Service type for --recommend-agents.")
    parser.add_argument("--phase", help="Lifecycle phase for --recommend-agents.")
    parser.add_argument("--run-next-queued", action="store_true", help="Execute the next queued run entry in FIFO order.")
    parser.add_argument("--worker-loop", action="store_true", help="Poll the local queue and execute queued runs until an exit condition is met.")
    parser.add_argument("--scheduled-for", help="ISO timestamp for when a queued run becomes eligible.")
    parser.add_argument("--schedule-delay-seconds", type=int, default=0, help="Delay before a queued run becomes eligible.")
    parser.add_argument("--retry-limit", type=int, default=1, help="Maximum number of retries allowed for a run lineage.")
    parser.add_argument("--poll-seconds", type=float, default=2.0, help="Sleep interval between idle queue polls in worker mode.")
    parser.add_argument("--max-runs", type=int, help="Maximum queued runs to execute before worker exit.")
    parser.add_argument("--max-idle-cycles", type=int, default=1, help="Maximum empty queue polls before worker exit.")
    args = parser.parse_args()

    if args.worker_loop:
        payload = _worker_loop(args)
    else:
        payload = _execute_once(args)
    _record_and_print(payload, args.pretty)


if __name__ == "__main__":
    main()
