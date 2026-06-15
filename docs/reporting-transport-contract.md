# Local Handoff Contract

The runtime renders GitHub-first handoff output under `codex_runtime_state/handoff/`.

## Principles

- GitHub and the local repository remain the source of truth.
- Handoff output is a local artifact for human review.
- No external dispatch is supported by default.
- Missing external services must never block validation.

## Runtime behavior

- `--prepare-reporting` renders the handoff markdown and summary text.
- The output may include GitHub delivery metadata, validation status, product state, strategy drafts, lessons learned, and self-improvement proposals.
- The runtime does not send messages to external networks.

## Failure behavior

- If handoff rendering fails, the run should report a local validation or file-writing issue.
- If GitHub delivery is not prepared, the handoff should say that PR artifacts were not created.
- Strategy and self-improvement sections remain drafts for human review.
