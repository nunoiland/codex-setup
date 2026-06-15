---
name: verification-loop
description: Turn failed tests, lint, builds, CI checks, browser QA, or repeated findings into reproducible evidence, fix hypotheses, and regression checks.
---

# Verification Loop

Use whenever validation fails or evidence is too weak to claim completion.

## Workflow

1. Capture the failing command or user flow.
2. Preserve the relevant log, screenshot, artifact, or error excerpt.
3. Reproduce the failure with the smallest command possible.
4. Identify the likely cause and one focused fix candidate.
5. Name a regression test or check that would prevent recurrence.
6. Re-run the same command or document the blocker.
7. Report pass, fail, skipped, and remaining risk honestly.

## Rules

- Do not retry without a new hypothesis.
- Do not claim success without rerunning the failing command or flow.
- Do not hide skipped validation.
- Do not install harness tools without a PRD and user approval.
- Keep evidence free of secrets and private data.

## Output

Return:

- failure summary
- reproduction command
- evidence path or excerpt
- suspected cause
- fix candidate
- regression candidate
- validation result
- follow-up risk
