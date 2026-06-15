# Live Validation Playbook

Use this playbook before trusting the runtime against real repositories.

GitHub and the local repository are the default path.

## Goals

- validate the live path with the smallest safe blast radius
- prove that credentials are injected correctly
- prove that GitHub remains the source of truth
- keep optional handoff delivery separate from default workflow validation

## Preconditions

- use a non-production test repository first
- confirm all secrets are injected externally
- confirm protected branches remain protected
- confirm `gh` and `git` are already authenticated if the current flow depends on local CLI auth

## Validation order

### 1. Dry-run and prepared output

Run:

```bash
python3 -m codex_runtime --prd <prd> --prepare-builders --prepare-github-delivery --cwd <repo> --pretty
```

Check:

- platform slices are correct
- builder commands are correct
- branch name is correct
- PR title and body path are correct
- blockers and warnings are understandable

### 2. Builder live validation

Use only test-safe builder commands first.

Run:

```bash
CODEX_ENABLE_BUILDER_EXECUTION=1 \
python3 -m codex_runtime --prd <prd> --execute-builders --cwd <repo> --pretty
```

Check:

- expected builder logs appear under `codex_runtime_state/builders/`
- builder outputs match the intended platform slices
- failure in one slice is reflected separately from the others

### 3. GitHub branch and PR validation

Start with a non-production repository.

If your local checkout still uses the public repository as `origin`, set:

```bash
export CODEX_GITHUB_REMOTE=validation-origin
```

Run:

```bash
CODEX_ENABLE_LIVE_GITHUB=1 \
python3 -m codex_runtime --prd <prd> --execute-github-delivery --cwd <repo> --pretty
```

Check:

- branch was created with the expected `codex/` name
- commit and push landed in the expected repository
- draft PR opened successfully
- PR body contains the expected handoff context
- protected branches were not mutated directly

### 4. Local handoff validation

```bash
python3 -m codex_runtime --prd <prd> --prepare-reporting --cwd <repo> --pretty
```

Check:

- handoff markdown was rendered locally
- handoff generation failure does not overwrite GitHub success
- warnings or errors are captured in the run record

### 5. End-to-end queued run validation

Queue one small run and process it through the worker loop.

```bash
python3 -m codex_runtime --prd <prd> --prepare-builders --prepare-github-delivery --cwd <repo> --pretty
python3 -m codex_runtime --cwd <repo> --worker-loop --max-runs 1 --max-idle-cycles 1 --poll-seconds 1 --pretty
```

Check:

- queue entry moved from `queued` to a terminal status
- run record was created
- builder and delivery artifacts line up with the same run

## Go / no-go checklist

Go only if:

- no tracked secrets were introduced
- builder logs look correct
- GitHub branch and draft PR match the intended repo
- local handoff artifact exists in the expected test workspace
- run record and handoff agree on status

Do not go if:

- the wrong repo, branch, or PR was targeted
- protected branch safety looks bypassed
- handoff output was written to the wrong workspace
- credentials had to be copied into tracked files
- run records are missing or inconsistent

## Promotion from test to real use

Promote in this order:

1. local dry-run
2. local live validation against a test repo
3. one small real repo run with human supervision
4. only then unattended overnight use
5. local handoff validation after the default GitHub-first path is proven

## Incident response

If the live path behaves unexpectedly:

1. stop the worker
2. rotate any suspected credentials
3. disable live env flags
4. preserve the run record and handoff
5. document the failure before retrying
