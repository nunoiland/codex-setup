from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

from .models import BuilderSliceExecution, RunPlan


COMMAND_ENV_BY_PLATFORM = {
    "web": "CODEX_WEB_BUILDER_COMMAND",
    "ios": "CODEX_IOS_BUILDER_COMMAND",
    "android": "CODEX_ANDROID_BUILDER_COMMAND",
    "api": "CODEX_API_BUILDER_COMMAND",
}


def _slugify(value: str) -> str:
    return "-".join(part for part in "".join(c.lower() if c.isalnum() else "-" for c in value).split("-") if part) or "prd-run"


def _context_env(plan: RunPlan, cwd: Path, platform: str) -> dict[str, str]:
    env = os.environ.copy()
    env["CODEX_RUNTIME_PRD_PATH"] = str(plan.prd_path)
    env["CODEX_RUNTIME_CWD"] = str(cwd)
    env["CODEX_RUNTIME_PLATFORM"] = platform
    env["CODEX_RUNTIME_PLATFORM_TARGET"] = plan.platform_target
    return env


def prepare_builder_execution(plan: RunPlan, cwd: str | Path, live_mode: bool = False) -> list[BuilderSliceExecution]:
    worktree = Path(cwd).resolve()
    run_slug = _slugify(plan.title)
    results: list[BuilderSliceExecution] = []
    for slice_ in plan.slices:
        env_name = COMMAND_ENV_BY_PLATFORM.get(slice_.platform, "")
        raw_command = os.getenv(env_name, "").strip() if env_name else ""
        log_path = worktree / "codex_runtime_state" / "builders" / run_slug / f"{slice_.platform}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        execution = BuilderSliceExecution(
            platform=slice_.platform,
            builders=slice_.builders,
            log_path=str(log_path),
        )
        if raw_command:
            execution.command = shlex.split(raw_command)
        else:
            execution.warnings.append(f"No builder command configured for {slice_.platform}; set {env_name}.")
        if live_mode and os.getenv("CODEX_ENABLE_BUILDER_EXECUTION") != "1":
            execution.warnings.append("Live builder execution is disabled. Set CODEX_ENABLE_BUILDER_EXECUTION=1 to execute.")
        results.append(execution)
    return results


def execute_builder_execution(plan: RunPlan, cwd: str | Path, prepared: list[BuilderSliceExecution]) -> list[BuilderSliceExecution]:
    worktree = Path(cwd).resolve()
    results: list[BuilderSliceExecution] = []
    for execution in prepared:
        if not execution.command:
            results.append(execution)
            continue
        if "Live builder execution is disabled. Set CODEX_ENABLE_BUILDER_EXECUTION=1 to execute." in execution.warnings:
            results.append(execution)
            continue
        env = _context_env(plan, worktree, execution.platform)
        process = subprocess.run(
            execution.command,
            cwd=str(worktree),
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        execution.executed = True
        execution.return_code = process.returncode
        combined = ""
        if process.stdout:
            combined += process.stdout
        if process.stderr:
            if combined:
                combined += "\n"
            combined += process.stderr
        Path(execution.log_path).write_text(combined)
        execution.success = process.returncode == 0
        if execution.success:
            execution.notes.append("Builder command completed successfully.")
        else:
            execution.errors.append(f"Builder command failed with exit code {process.returncode}.")
        results.append(execution)
    return results
