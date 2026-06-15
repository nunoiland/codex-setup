#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 - <<'PY'
from pathlib import Path
import json
import subprocess
import tomllib

required_files = [
    Path('AGENTS.md'),
    Path('README.md'),
    Path('docs/PRD.md'),
    Path('docs/TASK.md'),
    Path('docs/BUSINESS_RULES.md'),
    Path('docs/DESIGN.md'),
    Path('docs/design-reference-library.md'),
    Path('docs/design-system-contract.md'),
    Path('docs/senior-designer-review-checklist.md'),
    Path('docs/visual-qa-contract.md'),
    Path('docs/taste-and-copy-quality-contract.md'),
    Path('docs/role-plugin-operating-model.md'),
    Path('docs/agent-army-operating-model.md'),
    Path('docs/external-agent-army-source-review.md'),
    Path('docs/service-agent-routing-matrix.md'),
    Path('docs/agent-team-presets.md'),
    Path('docs/agent-copyright-attribution.md'),
    Path('docs/verification-loop-contract.md'),
    Path('docs/git-quality-tooling.md'),
    Path('docs/security-scanning-trivy.md'),
    Path('docs/template-bootstrap.md'),
    Path('docs/product-workspace-boundary.md'),
    Path('docs/public-release-checklist.md'),
    Path('docs/QA.md'),
    Path('.pre-commit-config.yaml'),
    Path('package.json'),
    Path('pnpm-lock.yaml'),
    Path('tsconfig.json'),
    Path('next-env.d.ts'),
    Path('next.config.ts'),
    Path('eslint.config.mjs'),
    Path('postcss.config.mjs'),
    Path('Dockerfile'),
    Path('docker-compose.yml'),
    Path('src/app/layout.tsx'),
    Path('src/app/page.tsx'),
    Path('src/app/app/page.tsx'),
    Path('src/app/admin/page.tsx'),
    Path('src/app/health/route.ts'),
    Path('src/config/product.ts'),
    Path('.codex/config.toml'),
    Path('.codex/instructions.md'),
    Path('.codex/hooks.json'),
    Path('.codex/hooks/guard.py'),
    Path('PRD/_template.md'),
    Path('PRD/2026-05-28-codex-external-pattern-optimization.md'),
    Path('PRD/2026-06-01-notification-command-removal.md'),
    Path('PRD/2026-06-01-git-quality-security-tooling.md'),
    Path('PRD/2026-06-02-template-repo-transition.md'),
    Path('PRD/2026-06-05-trivy-security-scanning.md'),
    Path('PRD/2026-06-06-agent-army-routing-layer.md'),
    Path('PRD/2026-06-14-product-workspace-boundary-hardening.md'),
    Path('PRD/2026-06-15-github-readme-finalization.md'),
    Path('PRD/2026-06-15-public-template-sanitization.md'),
    Path('PLANS/README.md'),
    Path('PLANS/2026-05-28-codex-external-pattern-optimization.md'),
    Path('PLANS/2026-06-01-notification-command-removal.md'),
    Path('PLANS/2026-06-01-git-quality-security-tooling.md'),
    Path('PLANS/2026-06-02-template-repo-transition.md'),
    Path('PLANS/2026-06-05-trivy-security-scanning.md'),
    Path('PLANS/2026-06-06-agent-army-routing-layer.md'),
    Path('PLANS/2026-06-14-product-workspace-boundary-hardening.md'),
    Path('PLANS/2026-06-15-github-readme-finalization.md'),
    Path('PLANS/2026-06-15-public-template-sanitization.md'),
    Path('docs/worktree-orchestration.md'),
    Path('docs/cron-runner.md'),
    Path('docs/how-to-use-codex-setting.md'),
    Path('docs/product-factory-operating-model.md'),
    Path('docs/product-factory-goal-contract.md'),
    Path('docs/product-factory-risk-register.md'),
    Path('docs/service-basecamp-architecture.md'),
    Path('docs/service-template-contract.md'),
    Path('docs/hermes-service-factory-contract.md'),
    Path('docs/vps-deployment-contract.md'),
    Path('docs/revenue-system-contract.md'),
    Path('docs/admin-observability-contract.md'),
    Path('docs/paperclip-operator-contract.md'),
    Path('docs/hermes-worker-contract.md'),
    Path('docs/paperclip-hermes-local-runbook.md'),
    Path('docs/graphiti-memory-contract.md'),
    Path('docs/future-codex-action.md'),
    Path('docs/external-agent-pattern-review.md'),
    Path('docs/codebase-knowledge-graph-contract.md'),
    Path('docs/external-tools-opt-in-runbook.md'),
    Path('codex_runtime/agent_routing.py'),
    Path('.github/workflows/pr-validate.yml'),
    Path('.github/workflows/nightly-harness.yml'),
    Path('.github/workflows/automerge.yml'),
    Path('scripts/worktree-init.sh'),
    Path('scripts/worktree-clean.sh'),
    Path('scripts/cron-runner.sh'),
    Path('scripts/browser-qa.sh'),
    Path('scripts/web-health-smoke.sh'),
    Path('scripts/product-workspace-audit.py'),
    Path('scripts/public-release-audit.py'),
    Path('scripts/bootstrap-template.py'),
    Path('scripts/harness-dry-run.sh'),
    Path('scripts/ci-pr-check.sh'),
    Path('scripts/github-automerge.py'),
    Path('.agents/skills/anti-slop-copy-review/SKILL.md'),
    Path('.agents/skills/frontend-taste-review/SKILL.md'),
    Path('.agents/skills/codebase-understanding/SKILL.md'),
    Path('.agents/skills/verification-loop/SKILL.md'),
]
missing = [str(path) for path in required_files if not path.is_file()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

config = tomllib.loads(Path('.codex/config.toml').read_text(encoding='utf-8'))
allowed_top_level = {
    'model',
    'review_model',
    'model_reasoning_effort',
    'personality',
    'approval_policy',
    'sandbox_mode',
    'model_instructions_file',
    'project_root_markers',
    'features',
    'agents',
}
unknown_top_level = sorted(set(config) - allowed_top_level)
if unknown_top_level:
    raise SystemExit(f"unsupported top-level config keys in repo config: {unknown_top_level}")

assert config['approval_policy'] == 'on-request', config['approval_policy']
assert config['sandbox_mode'] == 'workspace-write', config['sandbox_mode']
assert config['model_instructions_file'] == './instructions.md', config['model_instructions_file']
assert config['features'] == {'multi_agent': True, 'hooks': True}, config['features']
assert config['agents'] == {'max_threads': 6, 'max_depth': 1}, config['agents']

expected_agent_files = {
    'prd_orchestrator',
    'web_builder',
    'android_builder',
    'ios_builder',
    'api_builder',
    'qa_reviewer',
    'security_reviewer',
    'senior_product_designer',
    'copy_quality_reviewer',
    'codebase_cartographer',
    'verification_loop_specialist',
    'product_manager',
    'business_analyst',
    'market_researcher',
    'competitive_intelligence',
    'business_model_strategist',
    'pricing_revenue_strategist',
    'ux_researcher',
    'ux_architect',
    'brand_guardian',
    'frontend_ux_engineer',
    'solution_architect',
    'backend_reliability_engineer',
    'devops_sre_specialist',
    'database_optimizer',
    'ai_integration_engineer',
    'test_architect',
    'api_tester',
    'compliance_risk_reviewer',
    'observability_specialist',
    'growth_marketer',
    'app_store_optimizer',
    'sales_strategy_reviewer',
    'customer_success_reviewer',
    'technical_writer',
    'story_delivery_manager',
}
for agent_name in expected_agent_files:
    path = Path('.codex/agents') / f'{agent_name}.toml'
    if not path.is_file():
        raise SystemExit(f"missing agent config for {agent_name}: {path}")

hooks = json.loads(Path('.codex/hooks.json').read_text(encoding='utf-8'))
expected_hook_events = {'SessionStart', 'PreToolUse', 'PostToolUse', 'Stop'}
actual_hook_events = set((hooks.get('hooks') or {}).keys())
if actual_hook_events != expected_hook_events:
    raise SystemExit(f"hook event mismatch: expected {sorted(expected_hook_events)}, got {sorted(actual_hook_events)}")

workflow_text = '\n'.join(
    path.read_text(encoding='utf-8')
    for path in sorted(Path('.github/workflows').glob('*.yml'))
)
if 'OPENAI_API_KEY' in workflow_text:
    raise SystemExit('phase-1 workflows must not require OPENAI_API_KEY')
if 'codex-action' in workflow_text:
    raise SystemExit('phase-1 workflows must not use openai/codex-action')
if 'pre-commit/action' in workflow_text:
    raise SystemExit('phase-1 workflows must not require pre-commit/action')
if 'gitleaks' in workflow_text.lower():
    raise SystemExit('phase-1 workflows must not run gitleaks in CI')
if 'GITLEAKS_LICENSE' in workflow_text:
    raise SystemExit('phase-1 workflows must not require GITLEAKS_LICENSE')
if 'security-events: write' in workflow_text:
    raise SystemExit('phase-1 Trivy workflow must not request SARIF security-events permission')
for expected in (
    'checks: write',
    'reviewdog/action-actionlint@v1.72.0',
    'reporter: github-pr-check',
    'fail_level: error',
    'pnpm/action-setup@v4',
    'actions/setup-node@v4',
    'pnpm install --frozen-lockfile',
):
    if expected not in workflow_text:
        raise SystemExit(f'missing actionlint/reviewdog workflow guard: {expected}')
for expected in (
    'aquasecurity/trivy-action@v0.36.0',
    'continue-on-error: true',
    'scan-type: fs',
    'scan-ref: .',
    'scanners: vuln,misconfig',
    'severity: HIGH,CRITICAL',
    'format: table',
    'output: codex_runtime_state/actions/security/trivy-pr-scan.txt',
    'exit-code: "0"',
    'mkdir -p codex_runtime_state/actions/security',
):
    if expected not in workflow_text:
        raise SystemExit(f'missing Trivy workflow guard: {expected}')
trivy_block = workflow_text.split('aquasecurity/trivy-action@v0.36.0', 1)[1].split('\n      - name:', 1)[0]
if 'secret' in trivy_block.lower():
    raise SystemExit('phase-1 Trivy workflow must not enable CI secret scanning')
if 'exit-code: "1"' in trivy_block or "exit-code: '1'" in trivy_block:
    raise SystemExit('phase-1 Trivy workflow must remain non-blocking')
workflow_lower = workflow_text.lower()
for optional_service in (
    'paperclip',
    'hermes',
    'graphiti',
    'stripe',
    'toss',
    'caddy',
    'postgres',
    'storybook',
    'chromatic',
    'figma',
    'bmad',
    'agency-swarm',
    'metagpt',
    'chatdev',
):
    if optional_service in workflow_lower:
        raise SystemExit(f'phase-1 workflows must not require optional {optional_service} services')

agent_army_doc = Path('docs/agent-copyright-attribution.md').read_text(encoding='utf-8')
for expected in (
    'Do not copy external agent prompt bodies',
    'locally rewritten',
    'BMAD trademark notice',
):
    if expected not in agent_army_doc:
        raise SystemExit(f'missing Agent Army attribution boundary: {expected}')

precommit_text = Path('.pre-commit-config.yaml').read_text(encoding='utf-8')
for expected in (
    'repo: https://github.com/pre-commit/pre-commit-hooks',
    'rev: v6.0.0',
    'id: check-yaml',
    'id: check-toml',
    'id: check-json',
    'id: end-of-file-fixer',
    'id: trailing-whitespace',
    'id: check-merge-conflict',
    'id: check-added-large-files',
    'repo: https://github.com/gitleaks/gitleaks',
    'rev: v8.24.2',
    'id: gitleaks',
    'stages: [pre-commit]',
):
    if expected not in precommit_text:
        raise SystemExit(f'missing expected pre-commit config: {expected}')

package_text = Path('package.json').read_text(encoding='utf-8')
for expected in (
    '"next": "16.2.7"',
    '"react": "19.2.4"',
    '"react-dom": "19.2.4"',
    '"validate:web": "pnpm lint && pnpm typecheck && pnpm build"',
    '"smoke:health": "bash ./scripts/web-health-smoke.sh"',
):
    if expected not in package_text:
        raise SystemExit(f'missing expected starter package config: {expected}')

bootstrap_preview = subprocess.run(
    [
        'python3',
        'scripts/bootstrap-template.py',
        '--slug',
        'sample-product',
        '--name',
        'Sample Product',
        '--dry-run',
    ],
    capture_output=True,
    text=True,
    check=True,
).stdout
if 'sample-product' not in bootstrap_preview or 'Sample Product' not in bootstrap_preview:
    raise SystemExit(f'unexpected bootstrap dry-run output: {bootstrap_preview}')

retired_needles = [
    'tele' + 'gram',
    'chat' + 'ops',
    'CODEX_' + 'TELE' + 'GRAM',
    'CODEX_' + 'CHAT' + 'OPS',
]
tracked_files = subprocess.run(
    ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
retired_hits = []
for raw_path in tracked_files:
    path = Path(raw_path)
    if path.parts and path.parts[0] == 'codex_runtime_state':
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except (FileNotFoundError, UnicodeDecodeError):
        continue
    lowered = text.lower()
    for needle in retired_needles:
        if needle.lower() in lowered:
            retired_hits.append(str(path))
            break
if retired_hits:
    raise SystemExit(f"retired notification references remain in tracked files: {retired_hits}")

help_payload = subprocess.run(
    ['python3', '-m', 'codex_runtime', '--help'],
    capture_output=True,
    text=True,
    check=True,
).stdout.lower()
for expected in ('--recommend-agents', '--service-type', '--phase'):
    if expected not in help_payload:
        raise SystemExit(f"missing Agent Army runtime help flag: {expected}")
for needle in retired_needles + ['execute' + '-reporting']:
    if needle.lower() in help_payload:
        raise SystemExit(f"retired runtime flag still appears in help: {needle}")

python_files = (
    sorted(Path('codex_runtime').rglob('*.py'))
    + sorted(Path('.codex/hooks').rglob('*.py'))
    + sorted(Path('scripts').glob('*.py'))
)
for path in python_files:
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')

print('config-and-python-ok')
PY

python3 scripts/product-workspace-audit.py
python3 scripts/public-release-audit.py

bash -n \
  scripts/worktree-init.sh \
  scripts/worktree-clean.sh \
  scripts/cron-runner.sh \
  scripts/browser-qa.sh \
  scripts/web-health-smoke.sh \
  scripts/harness-dry-run.sh \
  scripts/ci-pr-check.sh \
  scripts/validate.sh

if command -v codex >/dev/null 2>&1; then
  codex --help >/tmp/codex-help.txt
  codex features list >/tmp/codex-features.txt
elif [[ "${CODEX_VALIDATE_REQUIRE_CODEX:-0}" == "1" ]]; then
  echo "codex CLI is required because CODEX_VALIDATE_REQUIRE_CODEX=1" >&2
  exit 1
else
  echo "codex-cli-skipped"
fi

if ! command -v pnpm >/dev/null 2>&1; then
  echo "pnpm is required for the starter validation layer" >&2
  exit 1
fi

pnpm lint >/tmp/codex-setting-eslint.txt
pnpm typecheck >/tmp/codex-setting-typecheck.txt
pnpm build >/tmp/codex-setting-build.txt

python3 -m codex_runtime \
  --prd PRD/2026-04-11-example-product-prd-web-ios.md \
  --prepare-builders \
  --prepare-github-delivery \
  --prepare-reporting \
  --cwd . \
  --pretty >/tmp/codex-setting-validate.json

python3 -m codex_runtime --operator-readiness --pretty >/tmp/codex-setting-operator-readiness.json
CODEX_MEMORY_BACKEND=graphiti python3 -m codex_runtime --operator-readiness --pretty >/tmp/codex-setting-operator-readiness-graphiti.json
CODEX_HERMES_ADAPTER_MODE=paperclip python3 -m codex_runtime --operator-readiness --pretty >/tmp/codex-setting-operator-readiness-paperclip.json
CODEX_EXTERNAL_TOOLS_MODE=opt-in CODEX_UNDERSTAND_ANYTHING_MODE=local CODEX_VERIFICATION_LOOP_MODE=local python3 -m codex_runtime --operator-readiness --pretty >/tmp/codex-setting-operator-readiness-external-tools.json
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty >/tmp/codex-setting-agent-web-discovery.json
python3 -m codex_runtime --recommend-agents --service-type subscription_credit_saas --phase architecture --pretty >/tmp/codex-setting-agent-subscription-architecture.json
python3 -m codex_runtime --recommend-agents --service-type mobile_app --phase qa --pretty >/tmp/codex-setting-agent-mobile-qa.json
python3 -m codex_runtime --recommend-agents --service-type finance_sensitive --phase release --pretty >/tmp/codex-setting-agent-finance-release.json

python3 - <<'PY'
from pathlib import Path
import json

default_payload = json.loads(Path('/tmp/codex-setting-operator-readiness.json').read_text(encoding='utf-8'))
if default_payload.get('memory', {}).get('backend') != 'json':
    raise SystemExit(f"unexpected default readiness payload: {default_payload}")
if default_payload.get('goal_contract', {}).get('command') != '/goal':
    raise SystemExit(f"missing /goal readiness contract: {default_payload}")
service_basecamp = default_payload.get('service_basecamp') or {}
if service_basecamp.get('status') != 'contract_ready':
    raise SystemExit(f"missing service basecamp readiness contract: {default_payload}")
if service_basecamp.get('template_scaffolded') is not False:
    raise SystemExit(f"service template should remain contract-only in this phase: {default_payload}")
if service_basecamp.get('monthly_vps_budget_krw_max', 0) > 100000:
    raise SystemExit(f"service basecamp budget must stay under 100000 KRW: {default_payload}")
design_layer = default_payload.get('design_layer') or {}
if design_layer.get('status') != 'contract_ready':
    raise SystemExit(f"missing design layer readiness contract: {default_payload}")
if design_layer.get('visual_qa_tooling_installed') is not False:
    raise SystemExit(f"visual QA tooling should remain contract-only in this phase: {default_payload}")
if design_layer.get('default_taste_anchor') != 'Midday':
    raise SystemExit(f"unexpected default design taste anchor: {default_payload}")
if default_payload.get('blockers'):
    raise SystemExit(f"default readiness should not block validation: {default_payload}")
if default_payload.get('risks'):
    raise SystemExit(f"default readiness should not have open optional setup risks: {default_payload}")
external_tools = default_payload.get('external_tools') or {}
if external_tools.get('mode') != 'off':
    raise SystemExit(f"external tools must default to off: {default_payload}")
if external_tools.get('understand_anything', {}).get('mode') != 'off':
    raise SystemExit(f"knowledge graph mode must default to off: {default_payload}")
if external_tools.get('taste_review', {}).get('status') != 'ready':
    raise SystemExit(f"taste review readiness missing: {default_payload}")
if external_tools.get('copy_review', {}).get('status') != 'ready':
    raise SystemExit(f"copy review readiness missing: {default_payload}")
if external_tools.get('verification_loop', {}).get('status') != 'contract_ready':
    raise SystemExit(f"verification loop should default to contract_ready: {default_payload}")
agent_army = default_payload.get('agent_army') or {}
if agent_army.get('status') != 'ready':
    raise SystemExit(f"missing Agent Army readiness: {default_payload}")
if agent_army.get('source_policy') != 'source_attributed_rewritten_roles':
    raise SystemExit(f"unexpected Agent Army source policy: {default_payload}")

graphiti_payload = json.loads(Path('/tmp/codex-setting-operator-readiness-graphiti.json').read_text(encoding='utf-8'))
if graphiti_payload.get('memory', {}).get('backend') != 'graphiti':
    raise SystemExit(f"unexpected graphiti readiness payload: {graphiti_payload}")
if graphiti_payload.get('blockers'):
    raise SystemExit(f"graphiti readiness should warn, not block validation: {graphiti_payload}")

paperclip_payload = json.loads(Path('/tmp/codex-setting-operator-readiness-paperclip.json').read_text(encoding='utf-8'))
if paperclip_payload.get('hermes_adapter', {}).get('mode') != 'paperclip':
    raise SystemExit(f"unexpected paperclip readiness payload: {paperclip_payload}")
if paperclip_payload.get('blockers'):
    raise SystemExit(f"paperclip readiness should warn, not block validation: {paperclip_payload}")
if not paperclip_payload.get('risks'):
    raise SystemExit(f"paperclip readiness should surface optional setup risks: {paperclip_payload}")
external_payload = json.loads(Path('/tmp/codex-setting-operator-readiness-external-tools.json').read_text(encoding='utf-8'))
if external_payload.get('blockers'):
    raise SystemExit(f"external tool readiness should warn, not block validation: {external_payload}")
external_section = external_payload.get('external_tools') or {}
if external_section.get('mode') != 'opt-in':
    raise SystemExit(f"unexpected external tool readiness payload: {external_payload}")
if external_section.get('understand_anything', {}).get('mode') != 'local':
    raise SystemExit(f"unexpected knowledge graph readiness payload: {external_payload}")
if external_section.get('verification_loop', {}).get('status') != 'local_optional':
    raise SystemExit(f"unexpected verification loop readiness payload: {external_payload}")

expected_agent_runs = {
    '/tmp/codex-setting-agent-web-discovery.json': ('web_saas', 'discovery', 'product_manager'),
    '/tmp/codex-setting-agent-subscription-architecture.json': ('subscription_credit_saas', 'architecture', 'payment_auth_specialist'),
    '/tmp/codex-setting-agent-mobile-qa.json': ('mobile_app', 'qa', 'android_builder'),
    '/tmp/codex-setting-agent-finance-release.json': ('finance_sensitive', 'release', 'compliance_risk_reviewer'),
}
for path_text, (service_type, phase, expected_agent) in expected_agent_runs.items():
    payload = json.loads(Path(path_text).read_text(encoding='utf-8'))
    if payload.get('service_type') != service_type or payload.get('phase') != phase:
        raise SystemExit(f"unexpected Agent Army routing payload: {payload}")
    agent_names = {
        item.get('name')
        for bucket in ('primary_agents', 'reviewer_agents', 'optional_agents')
        for item in payload.get(bucket, [])
    }
    if expected_agent not in agent_names:
        raise SystemExit(f"missing expected agent {expected_agent} in routing payload: {payload}")
    if not payload.get('validation_gates') or not payload.get('risks'):
        raise SystemExit(f"routing payload must include validation gates and risks: {payload}")
    if 'docs/agent-army-operating-model.md' not in payload.get('source_contracts', []):
        raise SystemExit(f"routing payload must include Agent Army source contract: {payload}")
print('operator-readiness-ok')
PY

CODEX_CRON_LOG_FILE=- \
CODEX_CRON_MODE=queue \
CODEX_CRON_MAX_RUNS=1 \
CODEX_CRON_MAX_IDLE_CYCLES=1 \
CODEX_CRON_POLL_SECONDS=0 \
CODEX_CRON_LOCK_DIR="/tmp/codex-setting-cron-validate-$$.lock" \
./scripts/cron-runner.sh >/tmp/codex-setting-cron-runner.json

python3 - <<'PY'
from pathlib import Path
import json

payload = json.loads(Path('/tmp/codex-setting-cron-runner.json').read_text(encoding='utf-8'))
if payload.get('worker_status') != 'idle_exit':
    raise SystemExit(f"unexpected cron runner validation payload: {payload}")
print('cron-runner-ok')
PY

CODEX_BROWSER_QA_ARTIFACT_DIR="/tmp/codex-setting-browser-qa-$$" ./scripts/browser-qa.sh >/tmp/codex-setting-browser-qa.txt
./scripts/harness-dry-run.sh --evidence-dir "/tmp/codex-setting-harness-$$" >/tmp/codex-setting-harness.txt

git diff --check

echo "validation-ok"
