# Runtime Memory Contract

The runtime stores durable operational memory under `codex_runtime_state/`.

## Memory types

### Run records

- path: `codex_runtime_state/runs/<run_id>.json`
- stores the full run snapshot, handoff pointers, strategy drafts, and execution metadata

### Queue entries

- path: `codex_runtime_state/queue/<run_id>.json`
- stores queued work plus scheduling and retry metadata

### Product-state memory

- path: `codex_runtime_state/pr/product-<service_slug>.json`
- stores a durable snapshot of product goal, target user, current stage, blockers, QA risks, growth experiments, pricing hypotheses, launch hypotheses, and next actions

### Self-improvement proposals

- path: `codex_runtime_state/pr/improvement-<run_id>.json`
- stores draft-only proposal sets that may later become skills, checklists, prompt updates, or guardrails after human review

## Principles

- memory should help the next run, not just archive the last one
- GitHub handoff remains canonical for human review, but runtime memory enables continuity across runs
- stale memory should be reviewed, deduplicated, or superseded over time
- any lesson that affects safety or release boundaries should be reviewed before adoption

## Minimum useful memory

- top blockers
- top warnings
- current stage
- QA risks
- next actions
- growth experiments already proposed
- pricing hypotheses already proposed
- launch hypotheses already proposed
