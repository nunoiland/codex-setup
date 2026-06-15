from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4


_SAFE_STORAGE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")


def _runtime_base(root: str | Path) -> Path:
    return Path(root).resolve() / "codex_runtime_state"


def _runs_dir(root: str | Path) -> Path:
    base = _runtime_base(root) / "runs"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _queue_dir(root: str | Path) -> Path:
    base = _runtime_base(root) / "queue"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _memory_dir(root: str | Path) -> Path:
    base = _runtime_base(root) / "pr"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _safe_storage_id(value: str, *, label: str) -> str:
    normalized = (value or "").strip()
    if not _SAFE_STORAGE_ID_RE.fullmatch(normalized):
        raise ValueError(f"Invalid {label}: {value!r}")
    return normalized


def _write_json(path: Path, payload: dict) -> str:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return str(path)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def schedule_for_delay(seconds: int | float | None) -> str:
    if not seconds:
        return ""
    delay = max(0, int(seconds))
    return (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat()


def save_run_record(root: str | Path, payload: dict) -> str:
    base = _runs_dir(root)
    run_id = _safe_storage_id(payload.get("run_id") or uuid4().hex[:12], label="run id")
    payload["run_id"] = run_id
    payload["recorded_at"] = _now()
    path = base / f"{run_id}.json"
    return _write_json(path, payload)


def load_run_record(root: str | Path, run_id: str) -> dict:
    run_id = _safe_storage_id(run_id, label="run id")
    path = _runs_dir(root) / f"{run_id}.json"
    return json.loads(path.read_text())


def list_run_records(root: str | Path) -> list[dict]:
    runs: list[dict] = []
    for path in sorted(_runs_dir(root).glob("*.json"), reverse=True):
        runs.append(json.loads(path.read_text()))
    return runs


def save_queue_entry(root: str | Path, payload: dict) -> str:
    base = _queue_dir(root)
    run_id = _safe_storage_id(payload.get("run_id") or uuid4().hex[:12], label="run id")
    payload["run_id"] = run_id
    payload["queued_at"] = _now()
    payload.setdefault("queue_status", "queued")
    path = base / f"{run_id}.json"
    return _write_json(path, payload)


def load_queue_entry(root: str | Path, run_id: str) -> dict:
    run_id = _safe_storage_id(run_id, label="run id")
    path = _queue_dir(root) / f"{run_id}.json"
    return json.loads(path.read_text())


def update_queue_entry(root: str | Path, run_id: str, updates: dict) -> str:
    run_id = _safe_storage_id(run_id, label="run id")
    payload = load_queue_entry(root, run_id)
    payload.update(updates)
    payload["updated_at"] = _now()
    path = _queue_dir(root) / f"{run_id}.json"
    return _write_json(path, payload)


def list_queue_entries(root: str | Path) -> list[dict]:
    entries: list[dict] = []
    for path in sorted(_queue_dir(root).glob("*.json"), reverse=True):
        entries.append(json.loads(path.read_text()))
    return entries


def _queue_sort_key(payload: dict) -> tuple[datetime, datetime, str]:
    scheduled = _parse_iso(payload.get("scheduled_for")) or datetime.min.replace(tzinfo=timezone.utc)
    queued = _parse_iso(payload.get("queued_at")) or datetime.min.replace(tzinfo=timezone.utc)
    return (scheduled, queued, payload.get("run_id", ""))


def next_queued_entry(root: str | Path) -> dict | None:
    now = datetime.now(timezone.utc)
    entries = list_queue_entries(root)
    eligible = [entry for entry in entries if entry.get("queue_status") == "queued"]
    eligible = [entry for entry in eligible if (_parse_iso(entry.get("scheduled_for")) or now) <= now]
    if not eligible:
        return None
    eligible.sort(key=_queue_sort_key)
    return eligible[0]


def save_product_state(root: str | Path, slug: str, payload: dict) -> str:
    slug = _safe_storage_id(slug, label="product slug")
    payload["updated_at"] = _now()
    path = _memory_dir(root) / f"product-{slug}.json"
    return _write_json(path, payload)


def load_product_state(root: str | Path, slug: str) -> dict:
    slug = _safe_storage_id(slug, label="product slug")
    path = _memory_dir(root) / f"product-{slug}.json"
    return json.loads(path.read_text())


def list_product_states(root: str | Path) -> list[dict]:
    states: list[dict] = []
    for path in sorted(_memory_dir(root).glob("product-*.json"), reverse=True):
        states.append(json.loads(path.read_text()))
    return states


def save_improvement_proposals(root: str | Path, run_id: str, payload: dict) -> str:
    run_id = _safe_storage_id(run_id, label="run id")
    payload["updated_at"] = _now()
    path = _memory_dir(root) / f"improvement-{run_id}.json"
    return _write_json(path, payload)


def load_improvement_proposals(root: str | Path, run_id: str) -> dict:
    run_id = _safe_storage_id(run_id, label="run id")
    path = _memory_dir(root) / f"improvement-{run_id}.json"
    return json.loads(path.read_text())
