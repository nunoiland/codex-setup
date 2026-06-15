# QA Checklist

## Required before calling work done
- Run `./scripts/validate.sh`.
- Run `./scripts/ci-pr-check.sh` when the change affects CI, GitHub delivery, harness behavior, or PR workflow.
- Run any extra validation required by the active PRD or plan.
- Inspect the diff for accidental secrets, unrelated edits, and approval-boundary drift.
- Confirm docs and config still match actual repo behavior.
- For UI-heavy work, run the senior designer review checklist and report screenshots or visual QA evidence when a runnable UI exists.
- For failed or flaky checks, apply [`verification-loop-contract.md`](./verification-loop-contract.md) before claiming the issue is understood.
- For public docs, landing pages, app copy, or handoffs, apply [`taste-and-copy-quality-contract.md`](./taste-and-copy-quality-contract.md) when tone quality matters.

## Review focus
- Correctness: does the change satisfy the PRD and task brief?
- Regression risk: did the change alter unrelated runtime or docs behavior?
- Security: were secret boundaries and approval rules preserved?
- Operability: can the next task start from docs without re-discovery?
- Design quality: does the UI satisfy the selected reference direction, accessibility, responsive behavior, and state requirements?

## If something was not validated
- Say exactly what was not run.
- Say why.
- Say the practical next check.
