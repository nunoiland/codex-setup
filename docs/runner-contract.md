# Runner Contract

This is the current dry-run runner contract for `codex-setting`.

## What exists now

- a PRD loader
- platform-target normalization
- platform-slice planning
- runtime auth readiness checks
- delivery and reporting readiness checks
- strategy draft generation for positioning, growth, revenue, launch, and ops
- product-state memory generation
- lessons-learned and self-improvement proposal drafts
- JSON dry-run output through `python3 -m codex_runtime --prd <path>`
- opt-in GitHub delivery preparation through `--prepare-github-delivery`
- opt-in reporting preparation through `--prepare-reporting`
- opt-in builder preparation through `--prepare-builders`
- local run-record persistence under `codex_runtime_state/runs/`
- local queue persistence under `codex_runtime_state/queue/`
- local product-state persistence under `codex_runtime_state/pr/product-*.json`
- local self-improvement draft persistence under `codex_runtime_state/pr/improvement-*.json`
- CLI resume and retry support using recorded execution requests
- one-shot dequeue worker via `--run-next-queued`
- bounded polling worker loop via `--worker-loop`
- delayed queue scheduling using `scheduled_for` metadata
- local cron-safe one-shot wrapper through `scripts/cron-runner.sh`
- direct status inspection via `--show-run`, `--show-queue`, `--show-product-state`, and `--show-improvement-proposals`
- operator readiness reporting for optional Paperclip, Hermes, and Graphiti services
- service basecamp contract readiness for future web-first services

## What this runner still does not do

- autonomous production deployment
- install or mutate system crontab entries
- multi-host schedulers or daemon orchestration beyond bounded local loops and the local cron wrapper
- auto-merge of self-improvement proposals
- live publishing to WordPress, Threads, X, video providers, or stock systems
- broad external-channel routing beyond the current strategy and ops draft surface
- mandatory Paperclip, Hermes, Graphiti, Neo4j, or Docker setup for normal PR validation
- actual service template scaffolding, live billing, live auth, or production deployment

## Why

This phase is intentionally conservative:

- auth-sensitive integrations need explicit approval
- the repository should prove memory, strategy, and queue semantics before broader automation
- strategy and self-improvement output must remain human-reviewed drafts
- GitHub and local handoff responsibilities must stay clearly separated

## Current output shape

The dry-run JSON includes:

- PRD path and title
- normalized platform target
- delivery mode
- reporting mode
- planned platform slices
- blockers and warnings
- auth readiness
- delivery readiness
- reporting readiness
- product-state memory
- strategy sections
- lessons learned
- self-improvement proposals
- operator notes

## Next implementation increment

The next safe increment should add:

1. richer long-running scheduler behavior
2. improved memory deduplication and recency rules
3. stronger product-state updates from real build and QA outcomes
4. operator-reviewed promotion of high-signal lessons into reusable skills
5. future publishing phases only after the current strategy/runtime layer is stable
